# Container Analysis

This directory contains a script to output Software Bill of Materials (SBOM)tree and vulnerabilities of running docker images.

## Prerequisites

The script depend on the [Syft](https://github.com/anchore/syft) project and the [Grype](https://github.com/anchore/grype) project.

### Installing syft

```
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
```

### Installing grype

```
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin
```

## Usage

Once your docker containers are up and running just use:

```
./container-analysis.sh
```

Note: It takes time ...

You will find the results in the 'out' folder.

### Viewer

If you would like to see a kind of summary, please run:

```
cd viewer
npm install
npm start
```

... and view in your browser 

```
http://localhost:3000
```