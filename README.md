# NZBHydra2 Exporter

Prometheus exporter for [nzbhydra2](https://github.com/theotherp/nzbhydra2)

## Usage

Make sure you have a few environment variables set:

`NZBHYDRA_URL`

`NZBHYDRA_APIKEY`

`NZBHYDRA_INTERVA` - (Optional, default 300) - Seconds between metrics collections


Metrics will be available at `http://localhost:8998/metrics`
