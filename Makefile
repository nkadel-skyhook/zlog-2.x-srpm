#
# Build mock and local RPM versions of tools
#

# Assure that sorting is case sensitive
LANG=C

#MOCKS+=epel-7-i386
#MOCKS+=epel-6-i386
#MOCKS+=epel-5-i386
#MOCKS+=epel-4-i386

MOCKS+=epel-7-x86_64
MOCKS+=epel-6-x86_64
#MOCKS+=epel-5-x86_64
#MOCKS+=epel-4-x86_64

SPEC := zlog.spec
PKGNAME := zlog

all:: zlog.spec $(MOCKS)

#NAME and VERSION are from zlog.spec.in, BUILD_NUMBER is from Jenkins
zlog.spec: zlog.spec.in Makefile
	@echo "Generating $@"
	if [ -n "$$BUILD_NUMBER" ]; then \
	   echo "   Using Jenkins BUILD_NUMBER: $$BUILD_NUMBER"; \
	   	cat scripts/zlog.spec.in | \
	   	 sed "s/^Release:.*/Release:        $$BUILD_NUMBER%{?dist}/g" > \
	   $@; \
	else \
	   rsync -a zlog.spec.in zlog.spec; \
	fi

srpm:: zlog.spec FORCE
	@echo "Building SRPM with $(SPEC)"
	rm -f $(PKGNAME)*.src.rpm
	rpmbuild --define '_sourcedir $(PWD)' \
		--define '_srcrpmdir $(PWD)' \
		-bs $(SPEC) --nodeps

build:: srpm FORCE
	rm -rf rpmbuild
	mkdir rpmbuild rpmbuild/RPMS rpmbuild/RPMS/noarch rpmbuild/RPMS/x86_64 rpmbuild/RPMS/i386
	mkdir rpmbuild/SRPMS
	rpmbuild --rebuild --define "_topdir $$PWD/rpmbuid" `ls *.src.rpm | grep -v ^epel-`

$(MOCKS):: zlog.spec FORCE
	@if [ -e $@ -a -n "`find $@ -name \*.rpm`" ]; then \
		echo "Skipping RPM populated $@"; \
	else \
		echo "Building $@ RPMS with $(SPEC)"; \
		rm -rf $@; \
		mock -q -r $@ --sources=$(PWD) \
		    --resultdir=$(PWD)/$@ \
		    --buildsrpm --spec=$(SPEC); \
		echo "Storing $@/*.src.rpm in $@.rpm"; \
		/bin/mv $@/*.src.rpm $@.src.rpm; \
		echo "Actally building RPMS in $@"; \
		rm -rf $@; \
		mock -q -r $@ \
		     --resultdir=$(PWD)/$@ \
		     $@.src.rpm; \
	fi

mock:: $(MOCKS)

clean::
	rm -rf $(MOCKS)
	rm -rf rpmbuild

realclean distclean:: clean
	rm -f *.src.rpm
	rm -f *.spec

FORCE:
