odoo.define('simplify_deepl_translator.Deepl', function (require) {
    'use strict';

    var translationDialog = require('web.TranslationDialog');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var session = require('web.session');

    var _t = core._t;

    translationDialog.include({

        init: function (parent, options) {
            options = options || {};

            this.fieldName = options.fieldName;
            this.domain = options.domain;
            this.searchName = options.searchName;
            this.userLanguageValue = options.userLanguageValue;
            this.domain.push(['name', "=", `${this.searchName}`]);
            this.dataPointID = options.dataPointID;
            this.isComingFromTranslationAlert = options.isComingFromTranslationAlert;
            this.currentInterfaceLanguage = session.user_context.lang;
            this.isText = options.isText;
            this.showSrc = options.showSrc;

            this._super(parent, _.extend({
                size: 'large',
                title: _.str.sprintf(_t('Translate: %s'), this.fieldName),
                buttons: [
                    { text: _t('Save'), classes: 'btn-primary', close: true, click: this._onSave.bind(this) },
                    { text: _t('Deepl'), classes: 'btn-primary', close: false, click: this.deepl.bind(this) },
                    { text: _t('Discard'), close: true },
                ],
            }, options));
        },

        deepl: function () {
            var self = this;
            var languages = [];
            var word = this.userLanguageValue;
            this.el.querySelectorAll('input[type=text],textarea').forEach((t) => {
                var initialValue = this.data.find((d) => d.id == t.dataset.id);
                languages.push([initialValue.lang.split('_')[1], initialValue.value]);
            });
            this._rpc({
                model: 'ir.translation',
                method: 'get_deepl_translation',
                args: [languages, word]
            }).then(function (translations) {
                var counter = 0;
                self.el.querySelectorAll('input[type=text],textarea').forEach((t) => {
                    $(t).val(translations[counter]);
                    counter++;
                });

            });
        }

    });


});