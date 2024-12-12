var tblResources, tblSearchResources, tblSeries;
var fvPurchase, fvProvider, fvSerie;
var select_provider;
var input_date_joined, input_search_resource, input_serie;

var purchase = {
    detail: {
        subtotal: 0.00,
        tax: 0.00,
        total_tax: 0.00,
        total_amount: 0.00,
        resources: [],
    },
    resource: null,
    calculateInvoice: function () {
        this.detail.resources.forEach(function (value, index, array) {
            value.index = index;
            if (value.is_equipment) {
                value.quantity = value.series.length;
            }
            value.subtotal = value.quantity * value.price;
        });
        this.detail.subtotal = this.detail.resources.reduce((a, b) => a + (b.subtotal || 0), 0);
        this.detail.total_tax = this.detail.subtotal * (this.detail.tax / 100);
        this.detail.total_amount = this.detail.subtotal + this.detail.total_tax;
        $('input[name="subtotal"]').val(this.detail.subtotal.toFixed(2));
        $('input[name="tax"]').val(this.detail.tax.toFixed(2));
        $('input[name="total_tax"]').val(this.detail.total_tax.toFixed(2));
        $('input[name="total_amount"]').val(this.detail.total_amount.toFixed(2));
    },
    // resource
    addResource: function (item) {
        this.detail.resources.push(item);
        this.listResources();
    },
    getResourcesIds: function () {
        return this.detail.resources.map(value => value.id);
    },
    listResources: function () {
        this.calculateInvoice();
        tblResources = $('#tblResources').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.detail.resources,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "code"},
                {data: "short_name"},
                {data: "quantity"},
                {data: "price"},
                {data: "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.is_equipment) {
                            return '<div class="input-group"><input type="text" class="form-control text-center" disabled value="' + row.series.length + '"><span class="input-group-append"><a class="btn btn-primary" rel="serie"><i class="fas fa-barcode"></i></a></span></div>';
                        }
                        return '<input type="text" class="form-control" autocomplete="off" name="quantity" value="' + row.quantity + '">';
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
                    targets: [-2],
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
                        max: 10000000
                    })
                    .on('keypress', function (e) {
                        return validate_text_box({'event': e, 'type': 'numbers'});
                    });
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    // serie
    addSerie: function (index, equipment) {
        purchase.detail.resources[index].series.push(equipment);
        this.listSeries(index);
    },
    getSeries: function () {
        return this.detail.resources.flatMap(value => value.series).map(value => value.serie);
    },
    listSeries: function (index) {
        var series = this.detail.resources[index].series.map((value, key) => ({index: key, serie: value.serie, guarantee: value.guarantee}));
        tblSeries = $('#tblSeries').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: series,
            columns: [
                {data: "index"},
                {data: "serie"},
                {data: "guarantee"},
            ],
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            info: false,
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" name="guarantee" autocomplete="off" value="' + row.guarantee + '">';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="guarantee"]')
                    .TouchSpin({
                        min: 1,
                        max: 100
                    })
                    .on('keypress', function (e) {
                        return validate_text_box({'event': e, 'type': 'numbers'});
                    });
            },
            initComplete: function (settings, json) {

            },
        });
    },
};

document.addEventListener('DOMContentLoaded', function (e) {
    fvPurchase = FormValidation.formValidation(document.getElementById('frmForm'), {
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
                number: {
                    validators: {
                        notEmpty: {},
                        digits: {},
                        stringLength: {
                            min: 8,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    number: fvPurchase.form.querySelector('[name="number"]').value,
                                    action: 'validate_purchase'
                                };
                            },
                            message: 'El número de factura ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                provider: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un proveedor'
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
            const iconPlugin = fvPurchase.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvPurchase.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            if (purchase.detail.resources.length === 0) {
                return message_error('Debe tener al menos un item en el detalle');
            }
            var params = new FormData(fvPurchase.form);
            params.append('detail', JSON.stringify(purchase.detail));
            var args = {
                'params': params,
                'form': fvPurchase.form,
            };
            submit_with_formdata(args);
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    fvProvider = FormValidation.formValidation(document.getElementById('frmProvider'), {
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
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    name: fvProvider.form.querySelector('[name="name"]').value,
                                    field: 'name',
                                    action: 'validate_provider'
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
                ruc: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 13
                        },
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    ruc: fvProvider.form.querySelector('[name="ruc"]').value,
                                    field: 'ruc',
                                    action: 'validate_provider'
                                };
                            },
                            message: 'El número de ruc ya se encuentra registrado',
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
                                    mobile: fvProvider.form.querySelector('[name="mobile"]').value,
                                    field: 'mobile',
                                    action: 'validate_provider'
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
                                    email: fvProvider.form.querySelector('[name="email"]').value,
                                    field: 'email',
                                    action: 'validate_provider'
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
            const iconPlugin = fvProvider.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvProvider.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var params = new FormData(fvProvider.form);
            params.append('action', 'create_provider');
            var args = {
                'params': params,
                'success': function (request) {
                    select_provider.select2('trigger', 'select', {data: request});
                    fvPurchase.revalidateField('provider');
                    $('#myModalProvider').modal('hide');
                }
            };
            submit_with_formdata(args);
        });
});

document.addEventListener('DOMContentLoaded', function (e) {
    fvSerie = FormValidation.formValidation(document.getElementById('frmSeries'), {
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
                serie: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    serie: fvSerie.form.querySelector('[name="serie"]').value,
                                    series: JSON.stringify(purchase.getSeries()),
                                    action: 'validate_serie'
                                };
                            },
                            message: 'El número de serie ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
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
            const iconPlugin = fvSerie.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fvSerie.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var serie = input_serie.val();
            purchase.addSerie(purchase.resource.index, {'serie': serie, 'guarantee': 1});
            fvSerie.resetForm(true);
            input_serie.val('').focus();
        });
});

$(function () {
    input_date_joined = $('input[name="date_joined"]');
    select_provider = $('select[name="provider"]');
    input_search_resource = $('input[name="search_resource"]');
    input_serie = $('input[name="serie"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es",
    });

    // Resources

    input_search_resource.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_resource',
                    'term': request.term,
                    'ids': JSON.stringify(purchase.getResourcesIds()),
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
            purchase.addResource(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearResources').on('click', function () {
        input_search_resource.val('').focus();
    });

    $('#tblResources tbody')
        .off()
        .on('click', 'a[rel="serie"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            purchase.resource = tblResources.row(tr.row).data();
            purchase.listSeries(purchase.resource.index);
            fvSerie.resetForm(true);
            $('#myModalSeries').modal('show');
        })
        .on('change', 'input[name="quantity"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            purchase.detail.resources[tr.row].quantity = parseInt($(this).val());
            purchase.calculateInvoice();
            $('td:last', tblResources.row(tr.row).node()).html('$' + purchase.detail.resources[tr.row].subtotal.toFixed(2));
        })
        .on('change', 'input[name="price"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            purchase.detail.resources[tr.row].price = parseFloat($(this).val());
            purchase.calculateInvoice();
            $('td:last', tblResources.row(tr.row).node()).html('$' + purchase.detail.resources[tr.row].subtotal.toFixed(2));
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblResources.cell($(this).closest('td, li')).index();
            purchase.detail.resources.splice(tr.row, 1);
            tblResources.row(tr.row).remove().draw();
            purchase.calculateInvoice();
            $('.tooltip').remove();
        });

    $('.btnSearchResources').on('click', function () {
        tblSearchResources = $('#tblSearchResources').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_resource',
                    'term': input_search_resource.val(),
                    'ids': JSON.stringify(purchase.getResourcesIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "code"},
                {data: "name"},
                {data: "resource_type.name"},
                {data: "price"},
                {data: "stock"},
                {data: "is_equipment"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success badge-pill">' + row.stock + '</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">' + row.stock + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.is_equipment) {
                            return '<span class="badge badge-primary badge-pill">Si</span>';
                        }
                        return '<span class="badge badge-info badge-pill">No</span>';
                    }
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
                // if (data.stock === 0) {
                //     $(row).addClass('low-stock');
                // }
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
        $('#myModalSearchResources').modal('show');
    });

    $('#myModalSearchResources').on('shown.bs.modal', function () {
        purchase.listResources();
    });

    $('#tblSearchResources tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchResources.row($(this).parents('tr')).data();
            row.quantity = 1;
            purchase.addResource(row);
            tblSearchResources.row($(this).parents('tr')).remove().draw();
        });

    $('.btnRemoveAllResources').on('click', function () {
        if (purchase.detail.resources.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                purchase.detail.resources = [];
                purchase.listResources();
            },
            'cancel': function () {

            }
        });
    });

    // Series

    $('#tblSeries tbody')
        .off()
        .on('change', 'input[name="guarantee"]', function () {
            var tr = tblSeries.cell($(this).closest('td, li')).index();
            purchase.detail.resources[purchase.resource.index].series[tr.row].guarantee = parseInt($(this).val());
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblSeries.cell($(this).closest('td, li')).index();
            var index = purchase.resource.index;
            purchase.detail.resources[index].series.splice(tr.row, 1);
            purchase.listSeries(index);
        });

    $('.btnRemoveAllSeries').on('click', function () {
        var index = purchase.resource.index;
        if (purchase.detail.resources[index].series.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                purchase.detail.resources[index].series = [];
                purchase.listSeries(index);
            },
            'cancel': function () {

            }
        });
    });

    $('.btnClearSerie').on('click', function () {
        fvSerie.resetForm(true);
        input_serie.val('').focus();
    });

    $('#myModalSeries').on('hidden.bs.modal', function () {
        purchase.listResources();
    });

    $('.btnGenerateSerie').on('click', function () {
        execute_ajax_request({
            'params': {
                'action': 'generate_random_serie'
            },
            'success': function (request) {
                purchase.addSerie(purchase.resource.index, {'serie': request.serie, 'guarantee': 1});
            }
        });
    });

    input_serie
        .on('keypress', function (e) {
            return validate_text_box({'event': e, 'type': 'numbers_letters'});
        })
        .on('keyup', function (e) {
            var value = $(this).val();
            $(this).val(value.toUpperCase());
        });

    // Search Provider

    select_provider.select2({
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
                    action: 'search_provider'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese un nombre o número de ruc',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            fvPurchase.revalidateField('provider');
        })
        .on('select2:clear', function (e) {
            fvPurchase.revalidateField('provider');
        });

    $('.btnAddProvider').on('click', function () {
        $('#myModalProvider').modal('show');
    });

    $('#myModalProvider').on('hidden.bs.modal', function () {
        fvProvider.resetForm(true);
    });

    $('input[name="ruc"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    $('input[name="mobile"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    // Form

    $('input[name="number"]').on('keypress', function (e) {
        return validate_text_box({'event': e, 'type': 'numbers'});
    });

    input_date_joined.datetimepicker({
        format: 'YYYY-MM-DD',
        useCurrent: false,
        locale: 'es',
        orientation: 'bottom',
        keepOpen: false
    });

    input_date_joined.on('change.datetimepicker', function (e) {
        fvPurchase.revalidateField('date_joined');
    });

    $('i[data-field="serie"]').hide();
    $('i[data-field="provider"]').hide();
    $('i[data-field="input_search_resource"]').hide();
});