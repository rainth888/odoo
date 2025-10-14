<template>
  <div class="config-system-management-system-services">
    <div
      class="form-item"
      :class="{ 'form-item--error': showPreviewConnectionCountWarning }"
    >
      <label class="form-item__label" for="preview-connection-count">预览连接数</label>
      <div class="form-item__body">
        <input
          id="preview-connection-count"
          ref="previewConnectionInput"
          class="form-item__input"
          type="number"
          min="0"
          inputmode="numeric"
          :value="previewConnectionCount"
          @input="handlePreviewConnectionCountInput"
          @blur="handlePreviewConnectionCountBlur"
          @focus="markPreviewConnectionCountTouched"
          :aria-invalid="showPreviewConnectionCountWarning ? 'true' : 'false'"
          :aria-describedby="
            showPreviewConnectionCountWarning
              ? previewConnectionCountErrorId
              : undefined
          "
          required
        />
        <p
          v-if="showPreviewConnectionCountWarning"
          class="form-item__error"
          :id="previewConnectionCountErrorId"
          role="alert"
        >
          预览连接数不能为空
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, defineComponent, ref, watch } from 'vue';

export default defineComponent({
  name: 'ConfigSystemManagementSystemServices',
  props: {
    modelValue: {
      type: Object,
      default: () => ({}),
    },
  },
  emits: ['update:modelValue', 'field-invalid'],
  setup(props, { emit }) {
    const previewConnectionInput = ref(null);
    const previewConnectionCount = ref('');
    const previewConnectionCountTouched = ref(false);
    const previewConnectionCountErrorId = 'preview-connection-count-error';

    const sanitizeNumeric = (value) => value.replace(/[^0-9]/g, '');

    watch(
      () => props.modelValue.previewConnectionCount,
      (value) => {
        const sanitized =
          value === undefined || value === null
            ? ''
            : sanitizeNumeric(String(value));
        if (sanitized !== previewConnectionCount.value) {
          previewConnectionCount.value = sanitized;
        }
      },
      { immediate: true }
    );

    const showPreviewConnectionCountWarning = computed(
      () => previewConnectionCountTouched.value && previewConnectionCount.value === ''
    );

    watch(
      showPreviewConnectionCountWarning,
      (invalid) => {
        emit('field-invalid', {
          field: 'previewConnectionCount',
          invalid,
        });
      },
      { immediate: true }
    );

    const syncPreviewConnectionCount = (value) => {
      const sanitized = sanitizeNumeric(value);
      previewConnectionCount.value = sanitized;
      emit('update:modelValue', {
        ...props.modelValue,
        previewConnectionCount:
          sanitized === '' ? null : Number.parseInt(sanitized, 10),
      });
    };

    const markPreviewConnectionCountTouched = () => {
      previewConnectionCountTouched.value = true;
    };

    const handlePreviewConnectionCountInput = (event) => {
      markPreviewConnectionCountTouched();
      const sanitized = sanitizeNumeric(event.target.value);
      if (sanitized !== event.target.value) {
        event.target.value = sanitized;
      }
      syncPreviewConnectionCount(sanitized);
    };

    const handlePreviewConnectionCountBlur = () => {
      markPreviewConnectionCountTouched();
      syncPreviewConnectionCount(previewConnectionCount.value);
    };

    return {
      previewConnectionInput,
      previewConnectionCount,
      showPreviewConnectionCountWarning,
      handlePreviewConnectionCountInput,
      handlePreviewConnectionCountBlur,
      markPreviewConnectionCountTouched,
      previewConnectionCountErrorId,
    };
  },
});
</script>

<style scoped>
.config-system-management-system-services {
  display: flex;
  flex-direction: column;
}

.form-item {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

.form-item__label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--label-color, #303133);
}

.form-item__body {
  display: flex;
  flex-direction: column;
}

.form-item__input {
  border: 1px solid var(--border-color, #dcdfe6);
  border-radius: 4px;
  padding: 6px 10px;
  font-size: 14px;
  line-height: 20px;
  transition: border-color 0.2s ease;
}

.form-item__input:focus {
  outline: none;
  border-color: var(--focus-border-color, #409eff);
}

.form-item--error .form-item__input {
  border-color: #f56c6c;
}

.form-item__error {
  color: #f56c6c;
  font-size: 12px;
  line-height: 18px;
  margin-top: 4px;
}
</style>
