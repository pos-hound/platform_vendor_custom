CUSTOM_BUILD_DATE := $(shell date -u +%Y%m%d-%H%M)

CUSTOM_PLATFORM_VERSION := 16.2

CUSTOM_VERSION := $(CUSTOM_BUILD)-$(CUSTOM_PLATFORM_VERSION)-$(CUSTOM_BUILD_DATE)
CUSTOM_VERSION_PROP := sixteen

# Additional Flags
PERF_ANIM_OVERRIDE ?= false

# PixelOS Platform Version
PRODUCT_PRODUCT_PROPERTIES += \
    ro.custom.build.date=$(CUSTOM_BUILD_DATE) \
    ro.custom.device=$(CUSTOM_BUILD) \
    ro.hound.maintainer=$(HOUND_MAINTAINER) \
    ro.custom.version=PixelOS_$(CUSTOM_VERSION)

ifeq ($(TARGET_INCLUDE_UPDATER),true)
PRODUCT_PRODUCT_PROPERTIES += \
    net.pixelos.build_type=ci \
    net.pixelos.version=$(CUSTOM_VERSION_PROP)

# Anim Override
PRODUCT_PRODUCT_PROPERTIES += \
    persist.sys.activity_anim_perf_override=$(PERF_ANIM_OVERRIDE)
