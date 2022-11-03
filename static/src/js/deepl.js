odoo.define('simplify_deepl_translator.Deepl', function (require) {
  'use strict';

  var translationDialog = require('web.TranslationDialog');
  var core = require('web.core');
  var Dialog = require('web.Dialog');
  var _t = core._t;

  translationDialog.include({
    xmlDependencies: (translationDialog.prototype.xmlDependencies || [])
    .concat(['/simplify_deepl_translator/static/src/xml/translate_dialog.xml']),
    events: _.extend({}, translationDialog.prototype.events, {
      'click .deepl_one': 'deeplOne'
    }),

    init: function (parent, options) {
      this._super.apply(this, arguments);
      this.buttons.splice(1, 0, { text: _t('Deepl'), classes: 'btn-primary', close: false, click: this.deeplAll.bind(this) });
    },

    deeplOne: function (event) {
      var $el = $(event.currentTarget);
      var term = $el.attr('term').split('_')[1];
      var value = $el.attr('value');
      var languages = [[term, value]];
      var word = this.userLanguageValue;
      this._rpc({
        model: 'ir.translation',
        method: 'get_deepl_translation',
        args: [languages, word]
      }).then(function (translations) {
        $el.parent().find('input, textarea').val(translations[0]);
      });
    },

    check_deepl_language_domain: function (language) {
      var language = language.split('_');
      language = language[language.length - 1];
      var deepl_target_languages = ['AU', 'BG', 'CA', 'CS', 'DA', 'DE', 'EL', 'EN', 'GB', 'US', 'ES', 'ET', 'FI', 'FR', 'HU', 'ID', 'IT', 'IN', 'JA', 'LT', 'LV', 'NL', 'PL', 'PT', 'PT-BR', 'PT-PT', 'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH'];
      if (deepl_target_languages.includes(language)) {
        return true;
      }
      return false;
    },


    deeplAll: function () {
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