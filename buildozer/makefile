BUILDOZER = buildozer

uninstall_apk:
	adb shell pm uninstall -k org.vaizlabs.android.cryptikchaos

purge_logs:
	rm -rf *.log

pre_build:
	sed -i 's/\(constants.ENABLE_TEST_MODE\s\+=\) True/\1 False/' ../src/cryptikchaos/env/configuration.py
	sed -i 's/\(constants.ENABLE_TLS\s\+=\) True/\1 False/' ../src/cryptikchaos/env/configuration.py

post_build:
	sed -i 's/\(constants.ENABLE_TEST_MODE\s\+=\) False/\1 True/' ../src/cryptikchaos/env/configuration.py
	sed -i 's/\(constants.ENABLE_TLS\s\+=\) False/\1 True/' ../src/cryptikchaos/env/configuration.py

build_apk: purge_logs pre_build
	$(BUILDOZER) --verbose android debug | tee -i build_apk.log

deploy_apk: uninstall_apk build_apk
	$(BUILDOZER) --verbose android deploy | tee -i deploy_apk.log

deploy: deploy_apk post_build

run: deploy
	$(BUILDOZER) --verbose android run | tee -i run_apk.log

test: run
	$(BUILDOZER) --verbose android logcat | awk '/I\/python/{print > "test_apk.log"} 1'

