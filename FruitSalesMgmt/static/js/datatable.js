
function set_datatable (id, order_i, asc_or_desc) {
    jQuery(function($){
        $(id).DataTable({
            lengthChange: false,
            searching: false,
            displayLength: 5,
            order: [ [ order_i, asc_or_desc ] ],
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
