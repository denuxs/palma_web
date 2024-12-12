var input_date_joined;
var select_production;
var tblTapeAssignments;
var fv;

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    },
                },
                production: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una producción'
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var detail = production.getTapeAssignments();
            if (detail.length === 0) {
                return message_error('Debe tener al menos un item seleccionado en el detalle');
            }
            var params = new FormData(fv.form);
            params.append('detail', JSON.stringify(detail));
            var args = {
                'params': params,
                'form': fv.form,
            };
            submit_with_formdata(args);
        });
});

var production = {
    activities: [],
    listTapeAssignments: function () {
        tblTapeAssignments = $('#tblTapeAssignments ').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: false,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_tape_assignment',
                    'id': select_production.val()
                },
                dataSrc: ""
            },
            order: [[0, 'desc']],
            columns: [
                {data: "id"},
                {data: "production_plant.plant.short_name"},
                {data: "production_plant.plant.lot.name"},
                {data: "tape"},
                {data: "id"},
                {data: "observations"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    ordering: false,
                    render: function (data, type, row) {
                        return '<input type="checkbox" name="selected" class="form-control-checkbox">';
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center'
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    ordering: false,
                    render: function (data, type, row) {
                        return '<div class="container-square" style="background-color: ' + row.tape.color + '"><span class="badge badge-secondary badge-pill">' + row.tape.week + '</span></div>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-left',
                    ordering: false,
                    render: function (data, type, row) {
                        return '<select class="form-control select2" style="width: 100%;" name="activity"></select>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    ordering: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="observations" autocomplete="off" placeholder="Ingrese una descripción" class="form-control" value="' + row.observations + '">';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="selected"]').prop('checked', data.selected === 1);
                tr.find('select[name="activity"]').select2({
                    data: production.activities,
                    theme: 'bootstrap4',
                    language: 'es'
                });
                if (!$.isEmptyObject(data.activity)) {
                    tr.find('select[name="activity"]').val(data.activity.id).trigger('change');
                }
            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getTapeAssignments: function () {
        if (tblTapeAssignments) return tblTapeAssignments.rows().data().toArray().filter(value => value.selected === 1);
        return [];
    }
};

$(function () {
    input_date_joined = $('input[name="date_joined"]');
    select_production = $('select[name="production"]');

    input_date_joined.datetimepicker({
        useCurrent: false,
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
    });

    input_date_joined.on('change.datetimepicker', function (e) {
        fv.revalidateField('date_joined');
    });

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    // Production

    $('#tblTapeAssignments  tbody')
        .off()
        .on('keyup', 'input[name="observations"]', function () {
            var tr = tblTapeAssignments.cell($(this).closest('td, li')).index();
            var data = tblTapeAssignments.row(tr.row).data();
            data.observations = $(this).val();
        })
        .on('change', 'select[name="activity"]', function () {
            var tr = tblTapeAssignments.cell($(this).closest('td, li')).index();
            var data = tblTapeAssignments.row(tr.row).data();
            data.activity = $(this).select2('data')[0];
        })
        .on('change', 'input[name="selected"]', function () {
            var tr = tblTapeAssignments.cell($(this).closest('td, li')).index();
            var data = tblTapeAssignments.row(tr.row).data();
            data.selected = this.checked ? 1 : 0;
        })

    $('input[name="select_all"]').on('change', function () {
        var checked = this.checked;
        if (tblTapeAssignments) {
            tblTapeAssignments.rows().every(function (rowIdx, tableLoop, rowLoop) {
                var data = this.data();
                data.selected = checked ? 1 : 0;
                var cell = this.cell(rowIdx, 0).node();
                $(cell).find('input[type="checkbox"][name="selected"]').prop('checked', checked);
            }).draw(false);
        }
    });

    select_production.on('change', function () {
        fv.revalidateField('production');
        production.listTapeAssignments();
    });
});