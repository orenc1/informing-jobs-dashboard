import json
import os

import requests as requests
from lxml import etree

from causes import causes_list, advanced_causes_list
from templates import javascript, table_head, style, links

TESTS_PREFIX = "https://gcsweb-ci.apps.ci.l2s4.p1.openshiftapps.com/gcs/origin-ci-test/logs/periodic-ci-openshift-release-master-nightly-"

INFORMING_JOBS = {
    "4.7-e2e-azure-deploy-cnv": "4.7-deploy",
    "4.7-e2e-azure-upgrade-cnv": "4.7-upgrade",
    "4.8-e2e-azure-deploy-cnv": "4.8-deploy",
    "4.8-e2e-azure-upgrade-cnv": "4.8-upgrade",
    "4.9-e2e-azure-deploy-cnv": "4.9-deploy",
    "4.9-e2e-azure-upgrade-cnv": "4.9-upgrade",
    "4.10-e2e-azure-deploy-cnv": "4.10-deploy",
    "4.10-e2e-azure-upgrade-cnv": "4.10-upgrade",
}

def load_data(test_jobs):
    for ij in INFORMING_JOBS:
        if os.path.isfile(f"results/{ij}.json"):
            with open(f"results/{ij}.json", 'r') as fh:
                test_jobs[ij] = json.load(fh)
    return test_jobs

def resolve_undetermined(test_jobs):
    for lane in test_jobs:
        for tj in test_jobs[lane]:
            if tj['reason'] == 'Undetermined':
                tj['reason'] = get_failure_reason(lane, tj['job_id'])
                if tj['reason'] != 'Undetermined':
                    print (f'INFO: reason for job {tj["job_id"]} in {lane} was updated to {tj["reason"]}.')


def collect_data(test_jobs):
    for ij in INFORMING_JOBS:
        html_response = requests.get(TESTS_PREFIX + ij).text
        i = 0
        tree = etree.HTML(html_response)
        all_elements = reversed(list(tree.iter()))
        for el in all_elements:
            if el.tag == 'img' and '..' not in el.tail and 'latest-build' not in el.tail:
                job_id = el.tail.strip()
                if len(test_jobs) > 0 and ij in test_jobs and job_exists(job_id, ij, test_jobs):
                    # We're iterating the jobs list in reversed order, so newest jobs will be parsed first.
                    # if we see a job that has already been parsed, we can stop for this lane.
                    print (f"job {job_id} already exist in {ij}")
                    break

                prowjob_response = requests.get(TESTS_PREFIX + ij + '/' + job_id + "prowjob.json").text
                prowjob = json.loads(prowjob_response)
                timestamp = prowjob["status"]["startTime"]
                test_result = prowjob["status"]["state"]
                if test_result == "pending":
                    continue
                job_url = prowjob["status"]["url"]

                if test_result == "failure":
                    reason = get_failure_reason(ij, job_id)
                else:
                    reason = ""
                tj = {
                    "job_id": job_id.replace('/', ''),
                    "job_url": job_url,
                    "timestamp": timestamp,
                    "result": test_result,
                    "reason": reason,
                }
                if ij not in test_jobs:
                    test_jobs[ij] = []
                test_jobs[ij].insert(0, tj)
                i += 1
                print (f'{str(i)}: {ij} from {tj["timestamp"]} added. Result: {tj["result"]}')
        with open(f'results/{ij}.json', 'w', encoding='utf-8') as fh:
            json.dump(test_jobs[ij], fh, indent=4)

    print ("Done.")


def render_html(test_jobs):
    for lane in test_jobs:
        seq = 1
        html = f"""
        <html>
            <head>
                <title>{lane}</title>
                <link href=https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.5.0/css/bootstrap.min.css rel=stylesheet>
                <link href=https://cdnjs.cloudflare.com/ajax/libs/datatables/1.10.20/css/dataTables.bootstrap4.min.css
          rel=stylesheet>
            </head>
            {style}
            <br>
            {links}
            <h1><b><center>Informing Jobs Results for: {lane}</center></b></h1>
            {table_head}
            """
        for tj in test_jobs[lane]:
            html += f"""
            <tr>
                <td>{str(seq)}</td>
                <td><a href={tj["job_url"]}>{tj["job_id"]}</a></td>
                <td>{tj["timestamp"]}</td>
                <td>{tj["result"]}</td>
                <td>{tj["reason"]}</td>
            </tr>
            """
            seq += 1
        html += f"""
            </tbody>
            </table>
            </html>
            {javascript}
            """
        with open(f"web/{lane}.html", 'w') as fh:
            fh.write(html)
            print(f"html for {lane} as been written to disk.")


def job_exists(job_id, test_name, test_jobs):
    for job in test_jobs[test_name]:
        if job["job_id"] == job_id.replace('/', '') and job["result"] != "pending":
            return True
    return False

def get_failure_reason(test_name, job_id):
    build_log = requests.get(TESTS_PREFIX + test_name + '/' + job_id + '/build-log.txt').text
    for line in build_log.splitlines():
        for cause in causes_list:
            if cause in line:
                return causes_list[cause]

    # regular cause could not be found, checking advanced
    line_num = -1
    for line in build_log.splitlines():
        line_num += 1
        for ac in advanced_causes_list:
            if ac[0][0] in line:
                is_match = False
                i = 1
                for aci in ac[0][1:]:
                    if aci in build_log.splitlines()[line_num+i]:
                        is_match = True
                        i += 1
                    else:
                        is_match = False
                        break
                if is_match:
                    return ac[1]

    print (f"Reason for failure of {test_name}/{job_id} has not been found.")
    return "Undetermined"


def create_dirs_if_not_exists(dirs):
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

def main():
    create_dirs_if_not_exists(["results", "web"])
    test_jobs = {}
    load_data(test_jobs)
    resolve_undetermined(test_jobs)
    collect_data(test_jobs)
    render_html(test_jobs)

if __name__ == '__main__':
    main()