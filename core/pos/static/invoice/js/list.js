var tbInvoice;
var input_date_range;
var invoice = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tbInvoice = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            order: [[0, 'desc']],
            columns: [
                {data: "id"},
                {data: "number"},
                {data: "client.names"},
                {data: "client.dni"},
                {data: "date_joined"},
                {data: "subtotal"},
                {data: "total_tax"},
                {data: "total_amount"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-5, 1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2, -3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a class="btn btn-success btn-xs btn-flat" rel="detail" data-toggle="tooltip" title="Detalle"><i class="fas fa-folder-open"></i></a> ';
                        buttons += '<a href="' + pathname + 'print/' + row.id + '/" target="_blank" data-toggle="tooltip" title="Imprimir" class="btn btn-secondary btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" data-toggle="tooltip" title="Eliminar" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    input_date_range = $('input[name="date_range"]');

    input_date_range
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                locale: {
                    format: 'YYYY-MM-DD',
                },
                autoApply: true,
            }
        )
        .on('change.daterangepicker apply.daterangepicker', function (ev, picker) {
            invoice.list(false);
        });

    $('.drp-buttons').hide();

    invoice.list(false);

    $('.btnSearchAll').on('click', function () {
        invoice.list(true);
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tbInvoice.cell($(this).closest('td, li')).index(),
                row = tbInvoice.row(tr.row).data();
            $('#tblPlants').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "plant_type.code"},
                    {data: "plant_type.name"},
                    {data: "quantity"},
                    {data: "price"},
                    {data: "subtotal"},
                ],
                columnDefs: [

                    {
                        targets: [-3],
                        class: 'text-center'
                    },
                    {
                        targets: [-1, -2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data.toFixed(2);
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalDetail').modal('show');
        });
});