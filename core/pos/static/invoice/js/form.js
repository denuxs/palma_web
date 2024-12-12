var tblPlants, tblSearchPlants;
var fvInvoice, fvClient;
var select_client;
var input_date_joined, input_search_plant;

var invoice = {
    detail: {
        subtotal: 0.00,
        tax: 0.00,
        total_tax: 0.00,
        total_amount: 0.00,
        plants: [],
    },
    calculateInvoice: function () {
        this.detail.plants.forEach(function (value, index, array) {
            value.subtotal = value.quantity * value.price;
        });
        this.detail.subtotal = this.detail.plants.reduce((a, b) => a + (b.subtotal || 0), 0);
        this.detail.total_tax = this.detail.subtotal * (this.detail.tax / 100);
        this.detail.total_amount = this.detail.subtotal + this.detail.total_tax;
        $('input[name="subtotal"]').val(this.detail.subtotal.toFixed(2));
        $('input[name="tax"]').val(this.detail.tax.toFixed(2));
        $('input[name="total_tax"]').val(this.detail.total_tax.toFixed(2));
        $('input[name="total_amount"]').val(this.detail.total_amount.toFixed(2));
    },
    // plants
    addPlant: function (item) {
        this.detail.plants.push(item);
        this.listPlants();
    },
    getPlantsIds: function () {
        return this.detail.plants.map(value => value.id);
    },
    listPlants: function () {
        this.calculateInvoice();
        tblPlants = $('#tblPlants').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.detail.plants,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "code"},
                {data: "name"},
                {data: "category.name"},
                {data: "stock"},
                {data: "quantity"},
                {data: "price"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-4, -5, 1],
                    class: 'text-center'
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="quantity" value="' + row.quantity + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="price" value="' + row.price + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="quantity"]')
                    .TouchSpin({
                        min: 1,
                        max: data.stock
                    })
                    .on('keypress', function (e) {
                        return validate_text_box({'event': e, 'type': 'numbers'});
                    });
                tr.find('input[name="price"]')
                    .TouchSpin({
                        min: 0.00,
                        max: 1000000,
                        step: 0.01,
                        decimals: 2,
                        boostat: 5,
                        maxboostedstep: 10,
                    })
                    .on('keypress', function (e) {
                        return validate_text_box({'event': e, 'type': 'numbers'});
                    });
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', function (e) {
    fvInvoice = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                client: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un cliente'
                        },
                    }
                },
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                }
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
            const iconPlugin = fvInvoice.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvInvoice.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            if (invoice.detail.plants.length === 0) {
                return message_error('Debe tener al menos un item en el detalle');
            }
            var params = new FormData(fvInvoice.form);
            params.append('detail', JSON.stringify(invoice.detail));
            var args = {
                'params': params,
                'form': fvInvoice.form,
            };
            submit_with_formdata(args);
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    fvClient = FormValidation.formValidation(document.getElementById('frmClient'), {
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
                names: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    names: fvClient.form.querySelector('[name="names"]').value,
                                    field: 'names',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                dni: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    dni: fvClient.form.querySelector('[name="dni"]').value,
                                    field: 'dni',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de cedula/ruc ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                mobile: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 10
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    mobile: fvClient.form.querySelector('[name="mobile"]').value,
                                    field: 'mobile',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El número de teléfono ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                email: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 5
                        },
                        regexp: {
                            regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                            message: 'El formato email no es correcto'
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    email: fvClient.form.querySelector('[name="email"]').value,
                                    field: 'email',
                                    action: 'validate_client'
                                };
                            },
                            message: 'El email ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                address: {
                    validators: {
                        enabled: false
                    }
                }
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
            const iconPlugin = fvClient.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvClient.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var params = new FormData(fvClient.form);
            params.append('action', 'create_client');
            var args = {
                'params': params,
                'success': function (request) {
                    select_client.select2('trigger', 'select', {data: request});
                    fvInvoice.revalidateField('client');
                    $('#myModalClient').modal('hide');
                }
            };
            submit_with_formdata(args);
        });
});

$(function () {
    input_date_joined = $('input[name="date_joined"]');
    select_client = $('select[name="client"]');
    input_search_plant = $('input[name="search_plant"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    // Plants

    input_search_plant.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_plant',
                    'term': request.term,
                    'ids': JSON.stringify(invoice.getPlantsIds()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.quantity = 1;
            invoice.addPlant(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearPlants').on('click', function () {
        input_search_plant.val('').focus();
    });

    $('#tblPlants tbody')
        .off()
        .on('change', 'input[name="quantity"]', function () {
            var tr = tblPlants.cell($(this).closest('td, li')).index();
            invoice.detail.plants[tr.row].quantity = parseInt($(this).val());
            invoice.calculateInvoice();
            $('td:last', tblPlants.row(tr.row).node()).html('$' + invoice.detail.plants[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="price"]', function () {
            var tr = tblPlants.cell($(this).closest('td, li')).index();
            invoice.detail.plants[tr.row].price = parseFloat($(this).val());
            invoice.calculateInvoice();
            $('td:last', tblPlants.row(tr.row).node()).html('$' + invoice.detail.plants[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblPlants.cell($(this).closest('td, li')).index();
            invoice.detail.plants.splice(tr.row, 1);
            tblPlants.row(tr.row).remove().draw();
            invoice.calculateInvoice();
            $('.tooltip').remove();
        });

    $('.btnSearchPlants').on('click', function () {
        tblSearchPlants = $('#tblSearchPlants').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_plant',
                    'term': input_search_plant.val(),
                    'ids': JSON.stringify(invoice.getPlantsIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "code"},
                {data: "name"},
                {data: "price"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center'
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchPlants').modal('show');
    });

    $('#myModalSearchPlants').on('shown.bs.modal', function () {
        invoice.listPlants();
    });

    $('#tblSearchPlants tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchPlants.row($(this).parents('tr')).data();
            row.quantity = 1;
            invoice.addPlant(row);
            tblSearchPlants.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllPlants').on('click', function () {
        if (invoice.detail.plants.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                invoice.detail.plants = [];
                invoice.listPlants();
            },
            'cancel': function () {

            }
        });
    });

    // Search Client

    select_client.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        width: null,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_client'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un nombre o número de cedula/ruc',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            fvInvoice.revalidateField('client');
        })
        .on('select2:clear', function (e) {
            fvInvoice.revalidateField('client');
        });

    $('.btnAddClient').on('click', function () {
        $('#myModalClient').modal('show');
    });

    $('#myModalClient').on('hidden.bs.modal', function () {
        fvClient.resetForm(true);
    });

    $('input[name="dni"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    $('input[name="mobile"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    // Form

    input_date_joined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_date_joined.on('change.datetimepicker', function (e) {
        fvInvoice.revalidateField('date_joined');
    });

    $('i[data-field="client"]').hide();
    $('i[data-field="input_search_plant"]').hide();
});