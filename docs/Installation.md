# Installation

## Binaries

This is the simplest method for installing CLI. Binaries for Wordfence CLI can be downloaded on the Releases page of the GitHub repository (under Assets of each release) along with source code and the .whl files:

[https://github.com/wordfence/wordfence-cli/releases](https://github.com/wordfence/wordfence-cli/releases)

The binary files are in the format `wordfence_x.x.x_yyyy_linux_exec.tar.gz` where `x.x.x` is the Wordfence CLI version, and `yyyy` is the CPU architecture. The following example uses `1.0.0` as the version, and `AMD64` as the architecture. 

If you'd like to go through the process of verifying the authenticity of the download, go through the steps below. **Otherwise, skip to the "Extract the binary" step.**

You can find our public key here:

	https://www.wordfence.com/wp-content/uploads/public.asc
	
To verify a signed binary, download both the gzipped binary and the .asc armor file for the architecture you've chosen.

	wget https://www.wordfence.com/wp-content/uploads/public.asc
	gpg --import public.asc

You can optionally sign the public key with your own private key:

	gpg --lsign-key 00B225C7030F26FF4A3D3481F82623ECE1DB0FBB

Each release asset has a .asc armor file that should be downloaded in addition to the binary. To verify the download run the following code (replace the file names with the ones you've downloaded):

	gpg --assert-signer 00B225C7030F26FF4A3D3481F82623ECE1DB0FBB --verify wordfence_1.0.0_amd64_linux_exec.tar.gz.asc wordfence_1.0.0_amd64_linux_exec.tar.gz

If your version of GPG doesn't include `--assert-signer` you can just run (you may see a warning using this method):

	gpg --verify wordfence_1.0.0_amd64_linux_exec.tar.gz.asc wordfence_1.0.0_amd64_linux_exec.tar.gz

You should see output similar to this:

	gpg: Signature made Fri Aug 18 16:27:11 2023 EDT
	gpg:                using EDDSA key 00B225C7030F26FF4A3D3481F82623ECE1DB0FBB
	gpg:                issuer "opensource@wordfence.com"
	gpg: Good signature from "Wordfence <opensource@wordfence.com>" [ultimate]
	gpg: signer '00B225C7030F26FF4A3D3481F82623ECE1DB0FBB' matched

Extract the binary:

	tar xvzf wordfence_1.0.0_amd64_linux_exec.tar.gz

Verify the binary works correctly on your system:

	./wordfence scan --version

You should see output similar to this:

	Wordfence CLI 1.0.0

Once this is done, we recommend [reviewing the configuration](Configuration.md) to go through configuring a license followed by [running your first scan](Examples.md).

## Docker

To install Wordfence CLI using Docker, you can clone the GitHub repo to your local environment:

	git clone git@github.com:wordfence/wordfence-cli.git
	cd ./wordfence-cli
	docker build -t wordfence-cli:latest .

Once the Docker image is built, you can start the docker container with the volumes you wish to scan:

	docker run -v /var/www:/var/www wordfence-cli:latest scan --version

You should see output similar to this:

	Wordfence CLI 1.0.0

Once this is done, we recommend [reviewing the configuration](Configuration.md) to go through configuring a license followed by [running your first scan](Examples.md).

## Manual Installation

To install Wordfence CLI manually, you can clone the GitHub repo to your local environment:

	git clone git@github.com:wordfence/wordfence-cli.git
	cd ./wordfence-cli
	pip install -r requirements.txt
	python setup.py
	python main.py scan --version

If you encounter an error about `libpcre.so` similar to this one:

	OSError: libpcre.so: cannot open shared object file: No such file or directory

You may need to install the `libpcre` library. 
