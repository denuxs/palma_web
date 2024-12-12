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
                color: {
                    validators: {
                        notEmpty: {},
                    },
                },
                name: {
                    validators: {
                        notEmpty: {}
                    }
                },
                description: {
                    validators: {
                        notEmpty: {
                            enabled: false
                        }
                    }
                },
                week: {
                    validators: {
                        notEmpty: {},
                        digits: {},
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    week: fv.form.querySelector('[name="week"]').value,
                                    field: 'week',
                                    action: 'validate_data'
                                };
                            },
                            message: 'La semana ya se encuentra registrada',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    },
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
            var args = {
                'params': new FormData(fv.form),
                'form': fv.form
            };
            submit_with_formdata(args);
        });
});

$(function () {
    $('input[name="color"]').colorpicker()
        .on('colorpickerChange colorpickerCreate', function (e) {
            fv.revalidateField('color');
        })
        .on('keyup', function () {
            $(this).colorpicker('setValue', $(this).val());
        });

    $('input[name="week"]')
        .TouchSpin({
            min: 1,
            max: 72,
            step: 1
        })
        .on('change touchspin.on.min touchspin.on.max', function () {
            fv.revalidateField('week');
        })
        .on('keypress', function (e) {
            return validate_text_box({'type': 'numbers', 'event': e});
        });

    $('i[data-field="week"]').hide();
});
