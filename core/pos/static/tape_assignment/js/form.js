var input_date_joined;
var select_production;
var tblPlants;
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
            var detail = production.getPlants();
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
    listPlants: function () {
        tblPlants = $('#tblPlants').DataTable({
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
                    'action': 'search_plant',
                    'id': select_production.val()
                },
                dataSrc: ""
            },
            order: [[0, 'desc']],
            columns: [
                {data: "id"},
                {data: "plant.short_name"},
                {data: "plant.lot.name"},
                {data: "id"}, // previus
                {data: "id"}, // next
                {data: "observations"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    ordering: false,
                    render: function (data, type, row) {
                        if (row.finalized) {
                            return '---';
                        }
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
                        if ($.isEmptyObject(row.previous)) {
                            return '---';
                        }
                        var content = '<div class="container-square" style="background-color: ' + row.previous.tape.color + '"><span class="badge badge-secondary badge-pill">' + row.previous.tape.week + '</span></div>';
                        content += '<span class="badge badge-secondary badge-pill">' + row.previous.date_joined + '</span>';
                        return content;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    ordering: false,
                    render: function (data, type, row) {
                        if (row.finalized) {
                            return '<span class="badge badge-secondary badge-pill">Finalizado</span>';
                        }
                        return '<div class="container-square" style="background-color: ' + row.next.color + '"><span class="badge badge-secondary badge-pill">' + row.next.week + '</span></div>';
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
                console.log(data);
                var tr = $(row).closest('tr');
                tr.find('input[name="selected"]').prop('checked', data.selected === 1);
            },
            initComplete: function (settings, json) {
                $('[data-toggle="tooltip"]').tooltip();
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getPlants: function () {
        if (tblPlants) return tblPlants.rows().data().toArray().filter(value => value.selected === 1);
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

    $('#tblPlants tbody')
        .off()
        .on('keyup', 'input[name="observations"]', function () {
            var tr = tblPlants.cell($(this).closest('td, li')).index();
            var data = tblPlants.row(tr.row).data();
            data.observations = $(this).val();
        })
        .on('change', 'input[name="selected"]', function () {
            var tr = tblPlants.cell($(this).closest('td, li')).index();
            var data = tblPlants.row(tr.row).data();
            data.selected = this.checked ? 1 : 0;
        })

    $('input[name="select_all"]').on('change', function () {
        var checked = this.checked;
        if (tblPlants) {
            tblPlants.rows().every(function (rowIdx, tableLoop, rowLoop) {
                var data = this.data();
                data.selected = checked ? 1 : 0;
                var cell = this.cell(rowIdx, 0).node();
                $(cell).find('input[type="checkbox"][name="selected"]').prop('checked', checked);
            }).draw(false);
        }
    });

    select_production.on('change', function () {
        fv.revalidateField('production');
        production.listPlants();
    });
});