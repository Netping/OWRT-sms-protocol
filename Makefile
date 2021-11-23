SECTION="NetPing modules"
CATEGORY="Base"
TITLE="EPIC OWRT-SMS-Protocol"

PKG_NAME="OWRT-SMS-Protocol"
PKG_VERSION="Epic.V0.S1"
PKG_RELEASE=1

CONF_FILE=smsprotoconf
CONF_DIR=/etc/config/

MODULE_FILES=smsproto.py
MODULE_FILES_DIR=/usr/lib/python3.7/

ETC_FILES=Configname
ETC_FILES_DIR=/etc/netping_sms_protocol/
ETC_FILES_COMMANDS=
ETC_FILES_COMMANDS_DIR=commands


.PHONY: all install

all: install
	
install:
	cp $(CONF_FILE) $(CONF_DIR)
	for f in $(MODULE_FILES); do cp $${f} $(MODULE_FILES_DIR); done
	mkdir $(ETC_FILES_DIR)
	for f in $(ETC_FILES); do cp etc/$${f} $(ETC_FILES_DIR); done
	mkdir $(ETC_FILES_DIR)$(ETC_FILES_COMMANDS_DIR)
	for f in $(ETC_FILES_COMMANDS); do cp etc/$${f} $(ETC_FILES_DIR)$(ETC_FILES_COMMANDS_DIR); done

clean:
	rm -f $(CONF_DIR)$(CONF_FILE)
	for f in $(MODULE_FILES); do rm -f $(MODULE_FILES_DIR)$${f}; done
	rm -rf $(ETC_FILES_DIR)
