top = $(abspath ../coreboot/)/

arch_files = src/arch/x86/acpi.c src/arch/x86/boot.c src/arch/x86/breakpoint.c src/arch/x86/cf9_reset.c src/arch/x86/cpu.c src/arch/x86/cpu_common.c src/arch/x86/ebda.c src/arch/x86/exception.c src/arch/x86/ioapic.c src/arch/x86/memcpy.c src/arch/x86/memmove_32.c src/arch/x86/memset.c src/arch/x86/mmap_boot.c src/arch/x86/null_breakpoint.c src/arch/x86/pirq_routing.c src/arch/x86/post.c src/arch/x86/postcar.c src/arch/x86/postcar_loader.c src/arch/x86/rdrand.c src/arch/x86/romstage.c src/arch/x86/smbios.c src/arch/x86/smbios_defaults.c src/arch/x86/tables.c src/arch/x86/timestamp.c

acpi_files = src/acpi/acpi.c src/acpi/acpi_pm.c src/acpi/acpigen.c src/acpi/acpigen_dptf.c src/acpi/acpigen_dsm.c src/acpi/acpigen_pci.c src/acpi/acpigen_ps2_keybd.c src/acpi/acpigen_usb.c src/acpi/device.c src/acpi/pld.c src/acpi/sata.c src/acpi/soundwire.c

commonlib_files = src/commonlib/bsd/cbfs_mcache.c src/commonlib/bsd/cbfs_private.c src/commonlib/bsd/elog.c src/commonlib/bsd/lz4_wrapper.c src/commonlib/iobuf.c src/commonlib/mem_pool.c src/commonlib/rational.c src/commonlib/region.c src/commonlib/sort.c


console_files = src/console/console.c src/console/die.c src/console/init.c src/console/post.c src/console/printk.c src/console/vsprintf.c src/console/vtxprintf.c

cpu_files = src/cpu/intel/car/romstage.c src/cpu/qemu-x86/bootblock.c src/cpu/qemu-x86/qemu.c src/cpu/x86/backup_default_smm.c src/cpu/x86/lapic/boot_cpu.c src/cpu/x86/lapic/lapic.c src/cpu/x86/mp_init.c src/cpu/x86/mtrr/debug.c src/cpu/x86/mtrr/earlymtrr.c src/cpu/x86/mtrr/mtrr.c src/cpu/x86/name/name.c src/cpu/x86/pae/pgtbl.c src/cpu/x86/smi_trigger.c src/cpu/x86/tsc/delay_tsc.c


device_files = src/device/cardbus_device.c src/device/cpu_device.c src/device/device.c src/device/device_const.c src/device/device_util.c src/device/dram/ddr2.c src/device/dram/ddr3.c src/device/dram/ddr4.c src/device/dram/ddr5.c src/device/dram/ddr_common.c src/device/dram/lpddr4.c src/device/dram/spd.c src/device/gpio.c src/device/i2c.c src/device/i2c_bus.c src/device/mdio.c src/device/mmio.c src/device/pci_class.c src/device/pci_device.c src/device/pci_early.c src/device/pci_ops.c src/device/pci_rom.c src/device/pciexp_device.c src/device/pcix_device.c src/device/pnp_device.c src/device/resource_allocator_common.c src/device/resource_allocator_v4.c src/device/root_device.c src/device/smbus_ops.c

drivers_files = src/drivers/emulation/qemu/bochs.c src/drivers/emulation/qemu/cirrus.c src/drivers/emulation/qemu/qemu_debugcon.c src/drivers/mipi/panel.c src/drivers/pc80/pc/i8254.c src/drivers/pc80/pc/i8259.c src/drivers/pc80/pc/isa-dma.c src/drivers/pc80/pc/keyboard.c src/drivers/pc80/rtc/mc146818rtc.c src/drivers/pc80/rtc/mc146818rtc_boot.c src/drivers/pc80/vga/vga.c src/drivers/pc80/vga/vga_font_8x16.c src/drivers/pc80/vga/vga_io.c src/drivers/pc80/vga/vga_palette.c src/drivers/spi/bitbang.c src/drivers/spi/spi-generic.c src/drivers/uart/uart8250io.c src/drivers/uart/util.c src/drivers/wifi/generic/acpi.c src/drivers/wifi/generic/generic.c src/drivers/wifi/generic/smbios.c

lib_files = src/lib/b64_decode.c src/lib/boot_device.c src/lib/bootblock.c src/lib/bootmem.c src/lib/bootmode.c src/lib/cbfs.c src/lib/cbfs_master_header.c src/lib/cbmem_common.c src/lib/cbmem_console.c src/lib/compute_ip_checksum.c src/lib/coreboot_table.c src/lib/crc_byte.c src/lib/delay.c src/lib/dimm_info_util.c src/lib/dp_aux.c src/lib/edid.c src/lib/edid_fill_fb.c src/lib/fallback_boot.c src/lib/fmap.c src/lib/gcc.c src/lib/halt.c src/lib/hardwaremain.c src/lib/hexdump.c src/lib/hexstrtobin.c src/lib/imd.c src/lib/imd_cbmem.c src/lib/libgcc.c src/lib/list.c src/lib/lzma.c src/lib/lzmadecode.c src/lib/malloc.c src/lib/master_header_pointer.c src/lib/memchr.c src/lib/memcmp.c src/lib/memrange.c src/lib/prog_loaders.c src/lib/prog_ops.c src/lib/ramdetect.c src/lib/ramtest.c src/lib/region_file.c src/lib/reset.c src/lib/rmodule.c src/lib/romstage_handoff.c src/lib/rtc.c src/lib/selfboot.c src/lib/spd_bin.c src/lib/stack.c src/lib/string.c src/lib/timestamp.c src/lib/uuid.c src/lib/version.c src/lib/wrdd.c src/lib/xxhash.c

mainboard_files = src/mainboard/emulation/qemu-i440fx/acpi_tables.c src/mainboard/emulation/qemu-i440fx/bootmode.c src/mainboard/emulation/qemu-i440fx/fw_cfg.c src/mainboard/emulation/qemu-i440fx/irq_tables.c src/mainboard/emulation/qemu-i440fx/mainboard.c src/mainboard/emulation/qemu-i440fx/memmap.c src/mainboard/emulation/qemu-i440fx/northbridge.c src/mainboard/emulation/qemu-i440fx/romstage.c


soutbridge_files = src/southbridge/intel/common/reset.c src/southbridge/intel/common/rtc.c src/southbridge/intel/common/smbus.c src/southbridge/intel/common/smbus_ops.c src/southbridge/intel/i82371eb/acpi_tables.c src/southbridge/intel/i82371eb/bootblock.c src/southbridge/intel/i82371eb/early_pm.c src/southbridge/intel/i82371eb/early_smbus.c src/southbridge/intel/i82371eb/fadt.c src/southbridge/intel/i82371eb/i82371eb.c src/southbridge/intel/i82371eb/ide.c src/southbridge/intel/i82371eb/isa.c src/southbridge/intel/i82371eb/smbus.c src/southbridge/intel/i82371eb/usb.c

etc_files = src/security/memory/memory.c src/security/memory/memory_clear.c src/superio/common/conf_mode.c



files = ${arch_files} ${acpi_files} ${commonlib_files} ${console_files} ${cpu_files} ${device_files} ${drivers_files} ${lib_files} ${soutbridge_files} ${etc_files}


# src/cpu/x86/mp_init.c
excluded = 




tmp_files := ${files}
files = $(filter-out ${excluded}, ${tmp_files})


.PHONY: printall
printall: 
	@echo ${top}


.PHONY: patch
patch:
	for file in ${files}; do \
		python3 main.py "${top}$${file}" patch; \
	done


.PHONY: clean
clean:
	for file in ${files}; do \
		python3 main.py "${top}$${file}" clean; \
	done
