docker run -d --name="pyftpd" \
	-p 65500-65520:65500-65520 \
	-v /Users/cychong/work/useless/pyftpd.yaml:/etc/pyftpd.yaml \
	-v /Users/cychong/Dropbox/incoming/:/pyftpd/incoming \
	-v /Users/cychong/tmp/:/pyftpd/log \
	-e PYFTPD_PORT=65500 \
	-e PYFTPD_PASSIVE_PORT=65501-65520 \
	cychong/pyftpd
