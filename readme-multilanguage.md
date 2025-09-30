# Multi-Language POS Receipt Implementation Guide

## Overview
This guide provides detailed steps to implement multi-language support for the POS custom receipt module, supporting English, Japanese, and Chinese languages.

## Prerequisites
- Odoo 18 with POS module installed
- `pos_custom_receipt` module installed
- Administrator access to Odoo backend

## Step 1: Enable Multi-Language Support in Odoo

### 1.1 Install Language Packs
1. Go to **Settings** → **Translations** → **Languages**
2. Click **Install Language** button
3. Install the following languages:
   - **English (US)** - Default
   - **Japanese (ja_JP)**
   - **Chinese (Simplified) (zh_CN)**
   - **Chinese (Traditional) (zh_TW)**

### 1.2 Configure Company Languages
1. Go to **Settings** → **Users & Companies** → **Companies**
2. Open your company record
3. In the **Languages** section, add:
   - English (US)
   - Japanese
   - Chinese (Simplified)
   - Chinese (Traditional)
4. Set **Default Language** to English (US)
5. Save the record

## Step 2: Create Translation Files

### 2.1 Create Translation Directory Structure
Create the following directory structure in your module:
```
addons_custom/pos_custom_receipt/
├── i18n/
│   ├── pos_custom_receipt.pot
│   ├── ja.po
│   ├── zh_CN.po
│   └── zh_TW.po
```

### 2.2 Generate Translation Template
1. Go to **Settings** → **Translations** → **Application Terms** → **Generate Translation**
2. Select **Module**: `pos_custom_receipt`
3. Select **Language**: All languages
4. Click **Generate**

### 2.3 Create Translation Files

#### English (pos_custom_receipt.pot)
```pot
#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_slogan
msgid "Receipt Slogan"
msgstr ""

#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_promo_lines
msgid "Promo Lines"
msgstr ""

#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_footer_note
msgid "Footer Note"
msgstr ""
```

#### Japanese (ja.po)
```po
#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_slogan
msgid "Receipt Slogan"
msgstr "レシートスローガン"

#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_promo_lines
msgid "Promo Lines"
msgstr "プロモーション行"

#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_footer_note
msgid "Footer Note"
msgstr "フッターノート"
```

#### Chinese Simplified (zh_CN.po)
```po
#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_slogan
msgid "Receipt Slogan"
msgstr "收据标语"

#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_promo_lines
msgid "Promo Lines"
msgstr "宣传语"

#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_footer_note
msgid "Footer Note"
msgstr "页脚备注"
```

#### Chinese Traditional (zh_TW.po)
```po
#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_slogan
msgid "Receipt Slogan"
msgstr "收據標語"

#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_promo_lines
msgid "Promo Lines"
msgstr "宣傳語"

#. module: pos_custom_receipt
#: model:ir.model.fields,field_description:pos_custom_receipt.field_res_company__receipt_footer_note
msgid "Footer Note"
msgstr "頁腳備註"
```

## Step 3: Update Module Manifest

### 3.1 Update __manifest__.py
```python
# -*- coding: utf-8 -*-
{
    'name': 'POS Custom Receipt (Thermal Style)',
    'summary': '自定义 POS 小票样式，复用热敏票据风格',
    'version': '1.2.0',
    'category': 'Point of Sale',
    'author': 'Your Company',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['point_of_sale', 'sale_receipt_thermal'],
    'data': [
        'views/res_company_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_custom_receipt/static/src/xml/pos_custom_receipt.xml',
            'pos_custom_receipt/static/src/css/receipt.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

## Step 4: Create Company Field Views

### 4.1 Create res_company_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_company_form_inherit_pos_custom_receipt" model="ir.ui.view">
        <field name="name">res.company.form.inherit.pos.custom.receipt</field>
        <field name="model">res.company</field>
        <field name="inherit_id" ref="base.view_company_form"/>
        <field name="arch" type="xml">
            <xpath expr="//field[@name='company_registry']" position="after">
                <field name="receipt_slogan" string="Receipt Slogan" placeholder="Enter receipt slogan"/>
                <field name="receipt_promo_lines" string="Promo Lines" widget="text" placeholder="Enter promotional lines (one per line)"/>
                <field name="receipt_footer_note" string="Footer Note" widget="text" placeholder="Enter footer note"/>
                <field name="receipt_business_number" string="Business Number" placeholder="Enter business registration number"/>
            </xpath>
        </field>
    </record>
</odoo>
```

## Step 5: Update Receipt Template for Multi-Language

### 5.1 Update pos_custom_receipt.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates id="template" xml:space="preserve">
  <!-- Multi-language header -->
  <t t-name="pos_custom_receipt.ReceiptHeader" t-inherit="point_of_sale.ReceiptHeader" t-inherit-mode="extension">
    <xpath expr="." position="replace">
      <t t-set="company" t-value="props.data.company"/>
      <t t-set="company_name" t-value="(company &amp;&amp; (company.name || company.display_name)) || ''"/>
      <t t-set="lang" t-value="props.data.lang || 'en_US'"/>
      
      <div class="pos-receipt">
        <div class="center">
          <div class="bold" t-if="company_name" t-esc="company_name"/>
          <div t-if="company.phone">
            <t t-if="lang.startsWith('ja')">電話: </t>
            <t t-elif="lang.startsWith('zh')">电话: </t>
            <t t-else="">Phone: </t>
            <t t-esc="company.phone"/>
          </div>
          <t t-set="_bizno" t-value="company.receipt_business_number || company.vat || company.company_registry"/>
          <div t-if="_bizno">
            <t t-if="lang.startsWith('ja')">営業番号: </t>
            <t t-elif="lang.startsWith('zh')">营业编号: </t>
            <t t-else="">Business No: </t>
            <t t-esc="_bizno"/>
          </div>
          <t t-set="addr" t-value="(company.street || '') + (company.city ? (' ' + company.city) : '') + (company.state_id ? (' ' + company.state_id.name) : '') + (company.zip ? (' ' + company.zip) : '')"/>
          <div t-if="addr">
            <t t-if="lang.startsWith('ja')">住所: </t>
            <t t-elif="lang.startsWith('zh')">地址: </t>
            <t t-else="">Address: </t>
            <t t-esc="addr"/>
          </div>
          <t t-if="company.receipt_promo_lines">
            <br/>
            <t t-foreach="(company.receipt_promo_lines || '').split('\n')" t-as="line" t-key="line">
              <div t-if="line" t-esc="line"/>
            </t>
          </t>
          <div t-if="company.receipt_slogan">
            <br/>
            <div class="fw-bolder" t-esc="company.receipt_slogan"/>
          </div>
          <br/>
          <div>
            <t t-if="lang.startsWith('ja')">日付: </t>
            <t t-elif="lang.startsWith('zh')">日期: </t>
            <t t-else="">Date: </t>
            <t t-esc="new Date(order_date).toLocaleString()"/>
          </div>
          <div>
            <t t-if="lang.startsWith('ja')">番号: </t>
            <t t-elif="lang.startsWith('zh')">编号: </t>
            <t t-else="">Number: </t>
            <t t-esc="props.data.name || ''"/>
          </div>
          <div>
            <t t-if="lang.startsWith('ja')">レシート番号: </t>
            <t t-elif="lang.startsWith('zh')">收据号: </t>
            <t t-else="">Receipt No: </t>
            <t t-esc="props.data.name || ''"/>
          </div>
          <div>
            <t t-if="lang.startsWith('ja')">担当者: </t>
            <t t-elif="lang.startsWith('zh')">负责人: </t>
            <t t-else="">Cashier: </t>
            <t t-esc="props.data.cashier || ''"/>
          </div>
          <br/>
        </div>
      </div>
    </xpath>
  </t>
</templates>
```

## Step 6: Configure POS for Multi-Language

### 6.1 Set User Language
1. Go to **Settings** → **Users & Companies** → **Users**
2. Open the POS user record
3. Set **Language** to desired language (English/Japanese/Chinese)
4. Save the record

### 6.2 Configure POS Session
1. Go to **Point of Sale** → **Configuration** → **Point of Sale**
2. Open your POS configuration
3. In **Advanced Settings**, ensure **Multi-Language** is enabled
4. Save the configuration

## Step 7: Test Multi-Language Receipt

### 7.1 Test English Receipt
1. Set user language to English
2. Open POS session
3. Create a test order
4. Print receipt - should show English labels

### 7.2 Test Japanese Receipt
1. Set user language to Japanese
2. Open POS session
3. Create a test order
4. Print receipt - should show Japanese labels (日付, 番号, etc.)

### 7.3 Test Chinese Receipt
1. Set user language to Chinese
2. Open POS session
3. Create a test order
4. Print receipt - should show Chinese labels (日期, 编号, etc.)

## Step 8: Troubleshooting

### 8.1 Common Issues
- **Language not changing**: Restart Odoo server after language installation
- **Translation not showing**: Clear browser cache and restart POS session
- **Missing translations**: Check translation files are properly formatted

### 8.2 Debug Steps
1. Check browser console for JavaScript errors
2. Verify translation files are in correct directory
3. Ensure module is properly upgraded
4. Check Odoo logs for translation errors

## Step 9: Maintenance

### 9.1 Adding New Languages
1. Install new language pack in Odoo
2. Create new .po file in i18n directory
3. Add language condition in template
4. Test and deploy

### 9.2 Updating Translations
1. Update .po files with new translations
2. Restart Odoo server
3. Clear POS cache
4. Test updated translations

## Conclusion
This implementation provides full multi-language support for POS receipts in English, Japanese, and Chinese. The system automatically detects the user's language and displays appropriate labels and formatting for each language.






