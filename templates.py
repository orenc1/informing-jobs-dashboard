style = """
    <style>
        div.dataTables_wrapper {
            margin: 0 auto;
            width: 70%;
        }
        table#results-table.dataTable tbody tr.Failure {
            background-color: #ffb3b3;
        }
        table#results-table.dataTable tbody tr.Success {
            background-color: #84e184;
        }        
    </style>
"""

links = """
    <center>
    <a href=4.7-e2e-azure-deploy-cnv.html>4.7-deploy</a><br>
    <a href=4.7-e2e-azure-upgrade-cnv.html>4.7-upgrade</a><br>
    <a href=4.8-e2e-azure-deploy-cnv.html>4.8-deploy</a><br>
    <a href=4.8-e2e-azure-upgrade-cnv.html>4.8-upgrade</a><br>
    <a href=4.9-e2e-azure-deploy-cnv.html>4.9-deploy</a><br>
    <a href=4.9-e2e-azure-upgrade-cnv.html>4.9-upgrade</a><br>
    <a href=4.10-e2e-azure-deploy-cnv.html>4.10-deploy</a><br>
    <a href=4.10-e2e-azure-upgrade-cnv.html>4.10-upgrade</a><br>
    <a href=4.11-e2e-azure-deploy-cnv.html>4.10-deploy</a><br>
    <a href=4.11-e2e-azure-upgrade-cnv.html>4.10-upgrade</a><br>
    <a href=4.12-e2e-azure-deploy-cnv.html>4.10-deploy</a><br>
    <a href=4.12-e2e-azure-upgrade-cnv.html>4.10-upgrade</a><br>
    </center>        
"""

javascript = """
            <script src=https://code.jquery.com/jquery-3.5.1.js></script>
            <script src=https://cdn.datatables.net/1.11.3/js/jquery.dataTables.min.js></script>
            <script src=https://cdn.datatables.net/1.11.3/js/dataTables.bootstrap4.min.js></script>
            <script>
                $(document).ready(function() {
                $('#results-table').DataTable( {
                    "pageLength": 100,
                    "lengthMenu": [ 10, 25, 50, 75, 100, 200 ],
                    "order": [[ 2, "desc" ]],
                    rowCallback: function (row, data) {
                      if (data[3] === 'failure') {
                        $(row).addClass('Failure');
                      }
                      if (data[3] === 'success') {
                        $(row).addClass('Success');
                      }                      
                    }                    
                } );
                } );
            </script>
            """

table_head = """
            <br>
            <table id="results-table" class="table table-striped table-bordered" style="width:100%">
            <thead>
                <tr>
                    <th>Seq</th>
                    <th>Job ID</th>
                    <th>Timestamp</th>
                    <th>Result</th>
                    <th>Reason</th>
                </tr>
            </thead>
            <tbody>
            """