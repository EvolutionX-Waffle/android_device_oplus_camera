#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

CAMERA_PATH := device/oplus/camera

# Permissions
PRODUCT_COPY_FILES += \
    $(CAMERA_PATH)/configs/permissions/oplus_google_lens_config.xml:$(TARGET_COPY_OUT_SYSTEM_EXT)/etc/permissions/oplus_google_lens_config.xml \
    $(CAMERA_PATH)/configs/permissions/privapp-permissions-oplus.xml:$(TARGET_COPY_OUT_SYSTEM_EXT)/etc/permissions/privapp-permissions-oplus.xml \
    $(CAMERA_PATH)/configs/sysconfig/hiddenapi-package-oplus-whitelist.xml:$(TARGET_COPY_OUT_SYSTEM)/etc/sysconfig/hiddenapi-package-oplus-whitelist.xml

# Properties
PRODUCT_SYSTEM_EXT_PROPERTIES += \
    oplus.software.camera.10bit=1 \
    ro.camera.disableHeicUltraHDR=1 \
    ro.com.google.lens.oem_camera_package=com.oplus.camera \
    ro.oplus.camera.defercap.all.quick.visible.support=1 \
    ro.oplus.camera.defercap.support=1 \
    ro.oplus.camera.facing.front.need.disable.nfc=1 \
    ro.oplus.camera.livephoto.support=1 \
    ro.oplus.camera.portrait.center.switch=oplus.switch.portrait.center \
    ro.oplus.camera.portrait_center.prefix=oplus.portrait.center. \
    ro.oplus.camera.speechassist=true \
    ro.oplus.camera.video.beauty.switch=oplus.switch.video.beauty \
    ro.oplus.camera.video_beauty.prefix=oplus.video.beauty. \
    ro.oplus.system.camera.name=com.oplus.camera

PRODUCT_VENDOR_PROPERTIES += \
    persist.vendor.camera.privapp.list=com.oplus.camera \
    vendor.camera.aux.packagelist=com.oplus.camera

$(call inherit-product, vendor/oplus/camera/camera-vendor.mk)
