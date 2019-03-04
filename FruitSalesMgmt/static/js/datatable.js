
function set_datatable (id) {
    jQuery(function($){
        $(id).DataTable({
            lengthChange: false,
            searching: false,
            ordering: false,
            displayLength: 5,
            language: {
                "url": "//cdn.datatables.net/plug-ins/1.10.19/i18n/Japanese.json",
                "sEmptyTable":     "テーブルにデータがありません",
                "sInfo":           " _TOTAL_ 件中 _START_ から _END_ まで表示",
                "oPaginate": {
                    "sFirst":    "先頭",
                    "sLast":     "最終",
                    "sNext":     "次",
                    "sPrevious": "前"
                },
            },
        });
    });
}
