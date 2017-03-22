INSTALL_PATH = /usr/local/bin
INSTALL_NAME = makeproj

install:
	mkdir -p $(INSTALL_PATH)
	cp makeproj.py $(INSTALL_PATH)/$(INSTALL_NAME)
	chmod +x $(INSTALL_PATH)/$(INSTALL_NAME)

uninstall:
	rm -f $(INSTALL_PATH)/$(INSTALL_NAME)
