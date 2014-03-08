uninstall_apk:
	adb shell pm uninstall -k org.vaizlabs.android.cryptikchaos

purge_logs:
	rm -rf *.log

apk: purge_logs
	buildozer android debug | tee -i build_apk.log

deploy: purge_logs uninstall_apk
	buildozer android debug deploy | tee -i deploy_apk.log

run: purge_logs uninstall_apk
	buildozer android debug deploy run | tee -i run_apk.log
