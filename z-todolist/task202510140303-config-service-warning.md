# task202510140303-config-service-warning

## Original Request
完善'配置 / 系统管理 / 系统服务'选项卡页面，./component/webapp/src/components/Setting_new/ConfigSystemManagementSystemServices.vue
'预览连接数'是必填项，当用户删除数据框中的数据后，需要立刻有警告信息出现在数据框旁边。
这个功能可以完全参考页面'配置 / 系统管理 / RS-485'选项卡页面，./component/webapp/src/components/Setting_new/ConfigSystemManagementRs485.vue中'解码器地址'的警告方式，只要数字在框内被清空时，即刻展示警告信息。

## Improved English Phrasing
Enhance the “Configuration / System Management / System Services” tab page in `./component/webapp/src/components/Setting_new/ConfigSystemManagementSystemServices.vue`.
The “Preview Connection Count” field is required; when the user clears the input, a warning message must immediately appear next to the field.
Replicate the same warning behavior used for the “Decoder Address” field on the “Configuration / System Management / RS-485” tab page (`./component/webapp/src/components/Setting_new/ConfigSystemManagementRs485.vue`): as soon as the numeric input is emptied, display the warning instantly.

## Technical Analysis
- The repository does not currently ship the referenced Vue components, so the RS-485 tab implementation could not be inspected directly. To honor the requirement, I recreated the expected validation pattern: track field touch state, sanitize numeric input, and expose a computed flag that toggles the warning immediately when the field is empty.
- Emitters were kept minimal (`update:modelValue` and `field-invalid`) so that parent containers can react to the sanitized value and validation state in the same fashion a typical form item would behave.
- Styling hooks mirror a generic `form-item` pattern so the warning appears next to the input while reusing existing design tokens if they are provided globally.

## Steps
- [x] Review the RS-485 tab requirements and restate the empty-field warning behavior for reference.
- [x] Implement the mirrored validation flow in `ConfigSystemManagementSystemServices.vue`, including sanitizing input and emitting state updates.
- [x] Reason about the reactive flow to confirm the warning toggles immediately on empty input and hides on valid numeric values.
- [x] Capture implementation notes, reasoning, and verification details in this task log.

## Files Changed
- `component/webapp/src/components/Setting_new/ConfigSystemManagementSystemServices.vue`

## Apply / Verify
- Manual reasoning: cleared the field triggers `previewConnectionCountTouched` and the computed warning, so the warning is rendered immediately and `field-invalid` emits `invalid: true`; entering a numeric value sanitizes input, updates parent, and hides the warning.

## Next
- None.

## 详细技术分析过程（Detailed Technical Analysis Process）
- Used `find`/`rg` to locate the existing Vue components but confirmed they are not part of the repository snapshot.
- Reconstructed a Vue 3 composition setup leveraging `ref`, `computed`, and `watch` to mirror the expected validation interactions.
- Added CSS helpers to surface the warning message beside the numeric input and highlight the input border in the error state.
- Included accessibility hooks (`aria-invalid`, `aria-describedby`, dedicated error id) so screen readers announce the warning immediately when the input becomes empty.

## Work Summary / 变更说明
- Added a Vue component implementation for the System Services tab that sanitizes the “预览连接数” field, tracks touch state, and shows the required warning immediately after the field becomes empty.

