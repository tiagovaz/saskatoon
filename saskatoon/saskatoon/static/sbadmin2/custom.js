    $(document).ready(function() {
        $('#dataTables-harvestlist').DataTable({
                responsive: true,
                "order": [[ 0, "desc" ]]
        });
        $('#dataTables-propertylist').DataTable({
                responsive: true,
                "order": [[ 0, "asc" ]]
        });
    });
