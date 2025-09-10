Place module translations here. Recommended workflow:

1) Start Odoo and enable Developer Mode.
2) Settings > Translations > Export Translation.
   - Language: en_US, ja, zh_CN
   - File Format: PO File
   - Apps To Export: Only this module (sale_receipt_thermal)
3) Save the generated files as:
   - i18n/en_US.po
   - i18n/ja.po
   - i18n/zh_CN.po
4) Edit the .po files to add translations, then upgrade module to load them.

Note: The PO entries must include module metadata and occurrences
      (Odoo adds these during export). Hand-written PO files without
      that context may fail to import.
