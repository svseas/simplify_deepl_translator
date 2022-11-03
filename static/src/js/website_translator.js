odoo.define('website_translator.translateMenu', async function (require) {
  'use strict';

  const { registry } = await require("@web/core/registry");
  var translateWidget = registry.category("website_navbar_widgets").get('TranslatePageMenu').Widget;
  var core = require('web.core');
  var _t = core._t;
  var rpc = require('web.rpc');

  translateWidget.include({

    translateBlock: async function (block, block_html, iso_code) {
      await rpc.query({
        model: 'ir.translation',
        method: "website_page_translation",
        args: [block_html, iso_code]
      }).then(function (translatedBlock) {
        block.html(translatedBlock);
        if (!block.hasClass('o_dirty')) {
          block.addClass('o_dirty');
        }
      });
    },

    _startTranslateMode: async function () {
      var self = this;
      var deepl = '<button class="btn btn-primary deepl_translate_all font-weight-bold"><span>' + _t('Translate') + '</span><img src="/simplify_deepl_translator/static/description/deepl_logo.png" width="30px" height="30px"/></button>';
      $("<div class='automatic_website_translator text-center m-3'>" + deepl + "</div>").insertAfter($('header').first());
      $(".deepl_translate_all").on("click", async function (event) {
        $.blockUI();
        var translatableContents = $('#wrapwrap .o_editable[data-oe-translation-state]');
        var iso_code = $('.js_change_lang.active').attr('data-url_code');
        for (var i = 0; i < translatableContents.length; i++) {
          var block = $(translatableContents[i]);
          await self.translateBlock(block, block.html(), iso_code);
        }
        $.unblockUI();
      });
      return this._super.apply(this, arguments);
    },

  });

});