var fv;
var input_date_range, input_search_contract, input_search_supply, input_search_equipment, input_search_plant;
var select_lot;
var tblContracts, tblSupplies, tblEquipment, tblPlants, tblSearchPlants, tblSearchContracts, tblSearchSupplies, tblSearchEquipment;

var production = {
    detail: {
        contracts: [],
        supplies: [],
        equipment: [],
        plants: [],
    },
    // Contract
    addContract: function (item) {
        this.detail.contracts.push(item);
        this.listContracts();
    },
    getContractIds: function () {
        return this.detail.contracts.map(value => value.id);
    },
    listContracts: function () {
        tblContracts = $('#tblContracts').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.detail.contracts,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "employee.names"},
                {data: "employee.dni"},
                {data: "employee.mobile"},
                {data: "employee.email"}
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3],
                    class: 'text-center'
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

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    // Supply
    addSupply: function (item) {
        this.detail.supplies.push(item);
        this.listSupplies();
    },
    getSuppliesIds: function () {
        return this.detail.supplies.map(value => value.id);
    },
    listSupplies: function () {
        tblSupplies = $('#tblSupplies').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.detail.supplies,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "code"},
                {data: "name"},
                {data: "resource_type.name"},
                {data: "stock"},
                {data: "quantity"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center'
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="quantity" value="' + row.quantity + '">';
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
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    // Equipment
    addEquipment: function (item) {
        this.detail.equipment.push(item);
        this.listEquipment();
    },
    getEquipmentIds: function () {
        return this.detail.equipment.map(value => value.id);
    },
    listEquipment: function () {
        tblEquipment = $('#tblEquipment').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.detail.equipment,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "resource.code"},
                {data: "resource.name"},
                {data: "resource.resource_type.name"},
                {data: "serie"},
                {data: "guarantee"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3, -4],
                    class: 'text-center'
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

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
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
                {data: "plant_type.name"},
                {data: "code"},
                {data: "plant_type.category.name"},
                {data: "lot.name"},
                {data: "latitude"},
                {data: "longitude"},
            ],
            columnDefs: [
                {
                    targets: [-1, -2, -3, -4, -5],
                    class: 'text-center'
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

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
};

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
                date_range: {
                    validators: {
                        notEmpty: {},
                        regexp: {
                            regexp: /^\d{4}-\d{2}-\d{2} - \d{4}-\d{2}-\d{2}$/,
                            message: 'El rango de fechas debe estar en el formato YYYY-MM-DD - YYYY-MM-DD',
                        }
                    }
                },
                lot: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un lote'
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
            if (production.detail.contracts.length === 0) {
                return message_error('Debe tener al menos un empleado en el detalle de la producción');
            }
            if (production.detail.plants.length === 0) {
                return message_error('Debe tener al menos una planta en el detalle de la producción');
            }
            var params = new FormData(fv.form);
            params.append('start_date', input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'));
            params.append('end_date', input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'));
            params.append('detail', JSON.stringify(production.detail));
            var args = {
                'params': params,
                'form': fv.form
            };
            submit_with_formdata(args);
        });
});

$(function () {
    input_date_range = $('input[name="date_range"]');
    input_search_contract = $('input[name="search_contract"]');
    input_search_supply = $('input[name="search_supply"]');
    input_search_equipment = $('input[name="search_equipment"]');
    input_search_plant = $('input[name="search_plant"]');
    select_lot = $('select[name="lot"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select')
        .on('change', function () {
            fv.revalidateField(this.name);
        });


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
            fv.revalidateField('date_range');
        });

    $('.drp-buttons').hide();

    // Contract

    input_search_contract.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_contract',
                    'term': request.term,
                    'ids': JSON.stringify(production.getContractIds()),
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
            production.addContract(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearContracts').on('click', function () {
        input_search_contract.val('').focus();
    });

    $('.btnRemoveAllContracts').on('click', function () {
        if (production.detail.contracts.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                production.detail.contracts = [];
                production.listContracts();
            },
            'cancel': function () {

            }
        });
    });

    $('#tblContracts tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblContracts.cell($(this).closest('td, li')).index();
            production.detail.contracts.splice(tr.row, 1);
            tblContracts.row(tr.row).remove().draw();
            $('.tooltip').remove();
        });

    $('.btnSearchContract').on('click', function () {
        tblSearchContracts = $('#tblSearchContracts').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_contract',
                    'term': input_search_contract.val(),
                    'ids': JSON.stringify(production.getContractIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "employee.names"},
                {data: "employee.dni"},
                {data: "employee.mobile"},
                {data: "employee.email"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, 0],
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
        $('#myModalSearchContracts').modal('show');
    });

    $('#tblSearchContracts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchContracts.row($(this).parents('tr')).data();
            row.quantity = 1;
            production.addContract(row);
            tblSearchContracts.row($(this).parents('tr')).remove().draw();
        });

    $('#myModalSearchContracts').on('shown.bs.modal', function () {
        production.listContracts();
    });

    // Resources

    input_search_supply.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_supply',
                    'term': request.term,
                    'ids': JSON.stringify(production.getSuppliesIds()),
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
            production.addSupply(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearSupply').on('click', function () {
        input_search_supply.val('').focus();
    });

    $('.btnRemoveAllSupplies').on('click', function () {
        if (production.detail.supplies.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                production.detail.supplies = [];
                production.listSupplies();
            },
            'cancel': function () {

            }
        });
    });

    $('#tblSupplies tbody')
        .off()
        .on('change', 'input[name="quantity"]', function () {
            var tr = tblSupplies.cell($(this).closest('td, li')).index();
            production.detail.supplies[tr.row].quantity = parseInt($(this).val());
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblSupplies.cell($(this).closest('td, li')).index();
            production.detail.supplies.splice(tr.row, 1);
            tblSupplies.row(tr.row).remove().draw();
            $('.tooltip').remove();
        });

    $('.btnSearchSupply').on('click', function () {
        tblSearchSupplies = $('#tblSearchSupplies').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_supply',
                    'term': input_search_supply.val(),
                    'ids': JSON.stringify(production.getSuppliesIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "code"},
                {data: "name"},
                {data: "resource_type.name"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, 0],
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
        $('#myModalSearchSupplies').modal('show');
    });

    $('#tblSearchSupplies tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchSupplies.row($(this).parents('tr')).data();
            row.quantity = 1;
            production.addSupply(row);
            tblSearchSupplies.row($(this).parents('tr')).remove().draw();
        });

    $('#myModalSearchSupplies').on('shown.bs.modal', function () {
        production.listSupplies();
    });

    // Equipment

    input_search_equipment.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_equipment',
                    'term': request.term,
                    'ids': JSON.stringify(production.getEquipmentIds()),
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
            production.addEquipment(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearEquipment').on('click', function () {
        input_search_equipment.val('').focus();
    });

    $('.btnRemoveAllEquipment').on('click', function () {
        if (production.detail.equipment.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                production.detail.equipment = [];
                production.listEquipment();
            },
            'cancel': function () {

            }
        });
    });

    $('#tblEquipment tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblEquipment.cell($(this).closest('td, li')).index();
            production.detail.equipment.splice(tr.row, 1);
            tblEquipment.row(tr.row).remove().draw();
            $('.tooltip').remove();
        });

    $('.btnSearchEquipment').on('click', function () {
        tblSearchEquipment = $('#tblSearchEquipment').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_equipment',
                    'term': input_search_equipment.val(),
                    'ids': JSON.stringify(production.getEquipmentIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "resource.code"},
                {data: "resource.name"},
                {data: "resource.resource_type.name"},
                {data: "serie"},
                {data: "guarantee"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, 0],
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
        $('#myModalSearchEquipment').modal('show');
    });

    $('#tblSearchEquipment tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchEquipment.row($(this).parents('tr')).data();
            row.quantity = 1;
            production.addEquipment(row);
            tblSearchEquipment.row($(this).parents('tr')).remove().draw();
        });

    $('#myModalSearchEquipment').on('shown.bs.modal', function () {
        production.listEquipment();
    });

    // Plant

    input_search_plant.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_plant',
                    'term': request.term,
                    'ids': JSON.stringify(production.getPlantsIds()),
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
            production.addPlant(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearPlant').on('click', function () {
        input_search_plant.val('').focus();
    });

    $('.btnRemoveAllPlants').on('click', function () {
        if (production.detail.plants.length === 0) return false;
        dialog_action({
            'content': '¿Estas seguro de eliminar todos los items de tu detalle?',
            'success': function () {
                production.detail.plants = [];
                production.listPlants();
            },
            'cancel': function () {

            }
        });
    });

    $('#tblPlants tbody')
        .off()
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblPlants.cell($(this).closest('td, li')).index();
            production.detail.plants.splice(tr.row, 1);
            tblPlants.row(tr.row).remove().draw();
            $('.tooltip').remove();
        });

    $('.btnSearchPlant').on('click', function () {
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
                    'ids': JSON.stringify(production.getPlantsIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "plant_type.name"},
                {data: "code"},
                {data: "plant_type.category.name"},
                {data: "lot.name"},
                {data: "latitude"},
                {data: "longitude"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2, -3, -4, 0],
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

    $('#tblSearchPlants tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var row = tblSearchPlants.row($(this).parents('tr')).data();
            row.quantity = 1;
            production.addPlant(row);
            tblSearchPlants.row($(this).parents('tr')).remove().draw();
        });

    $('#myModalSearchPlants').on('shown.bs.modal', function () {
        production.listPlants();
    });
});