<template>
  <div class="info-tooltip" @click="toggleTooltip" ref="tooltipRef">
    <i class="pi pi-info-circle"></i>
    <div class="tooltip-popup" :class="{ 'tooltip-popup--visible': isVisible }">
      <div class="tooltip-popup__content">
        <slot></slot>
      </div>
      <div class="tooltip-popup__arrow"></div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';

export default {
  name: 'InfoTooltip',
  
  setup() {
    const isVisible = ref(false);
    const tooltipRef = ref(null);
    
    // Toggle tooltip visibility
    const toggleTooltip = () => {
      isVisible.value = !isVisible.value;
    };
    
    // Close tooltip when clicking outside
    const handleOutsideClick = (event) => {
      if (tooltipRef.value && !tooltipRef.value.contains(event.target) && isVisible.value) {
        isVisible.value = false;
      }
    };
    
    // Add/remove click handler
    onMounted(() => {
      document.addEventListener('click', handleOutsideClick);
    });
    
    onBeforeUnmount(() => {
      document.removeEventListener('click', handleOutsideClick);
    });
    
    return {
      isVisible,
      tooltipRef,
      toggleTooltip
    };
  }
};
</script>

<style lang="scss" scoped>
.info-tooltip {
  position: relative;
  display: inline-flex;
  align-items: center;
  margin-left: 4px;
  
  i {
    font-size: 14px;
    color: #f7941d;
    cursor: pointer;
    background-color: rgba(247, 148, 29, 0.1);
    border-radius: 50%;
    width: 18px;
    height: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    
    &:hover {
      background-color: rgba(247, 148, 29, 0.2);
      transform: scale(1.1);
    }
  }
}

.tooltip-popup {
  position: absolute;
  top: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  padding: 10px 12px;
  min-width: 220px;
  max-width: 280px;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.2s ease;
  pointer-events: none;
  
  &--visible {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
  }
  
  &__content {
    font-size: 13px;
    line-height: 1.4;
    color: #333;
    text-align: left;
  }
  
  &__arrow {
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%) rotate(45deg);
    width: 12px;
    height: 12px;
    background-color: white;
    box-shadow: -2px -2px 4px rgba(0, 0, 0, 0.05);
  }
}
</style>