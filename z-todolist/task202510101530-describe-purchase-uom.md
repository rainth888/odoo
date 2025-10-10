# task202510101530-describe-purchase-uom

## Original Request
文档./doc/product_full_workflow_cn.md中下面的描述，详细说明一下如何找到`采购计量单位`这个操作位置。

## Improved English Phrasing
In the document `doc/product_full_workflow_cn.md`, expand the description to explain in detail how to locate the "Purchase Unit of Measure" field.

## Technical Analysis
- Need to edit the Chinese product workflow documentation section that describes unit-based products.
- Provide actionable navigation guidance in Odoo UI for locating the "Purchase Unit of Measure" (采购计量单位) setting on the product form.
- Ensure the explanation fits the context of the existing bullet list and maintains consistent formatting and tone.

## Steps
1. Review the relevant section of `doc/product_full_workflow_cn.md` to understand current wording and structure. ✅
2. Draft additional sentences or sub-bullets describing the navigation path to the Purchase UoM field. ✅
3. Update the document while keeping style and bilingual formatting consistent. ✅
4. Proofread formatting and ensure Markdown renders correctly. ✅

## Files Changed
- `doc/product_full_workflow_cn.md`
- `z-todolist/_todolis.md`
- `z-todolist/task202510101530-describe-purchase-uom.md`

## Apply / Verify
- Preview Markdown formatting locally (visual inspection). ✅

## Next
- None after documentation is updated and verified.

## Detailed Technical Analysis Process
- Located the "Unit-Based Products" subsection within the master data configuration chapter of `doc/product_full_workflow_cn.md`.
- Confirmed that the Purchase UoM field lives in the same block as the standard UoM field on the product form and that visibility depends on enabling Multi-Units of Measure.
- Added bilingual guidance explaining the exact position of the field and the prerequisite configuration so readers can navigate to it confidently.

## Work Summary / 变更说明
- 已在文档中补充“采购计量单位”字段所在位置及前置设置的说明，并完成格式校对。
