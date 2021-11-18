## Installation

### Mano Managed Entity Variables

#### NFVO
| NAME | VALUE |
| ------ | ------ |
| BASE_URL | /ubi-etsi-mano/ |
| HTTP_PORT | 8080 |

#### VNFM
| NAME | VALUE |
| ------ | ------ |
| BASE_URL | /ubi-etsi-mano/ |
| HTTP_PORT | 8080 |


### Workflows installation

```sh
cd /opt/fmc_repository/
git clone https://github.com/openmsa/Workflows.git ./Telekom_Malaysia
chown -R ncuser:ncuser ./Telekom_Malaysia
cd /opt/fmc_repository/Process/
ln -s ../Telekom_Malaysia/ETSI/Python Telekom_Malaysia
chown -R ncuser:ncuser Telekom_Malaysia
```

### Python libraries
#### For custom modules create softlink according to [the guide](https://ubiqube.com/wp-content/docs/2.4.1/developer-guide/developer-guide-single.html#_how_to_extend_the_sdk)

```sh
cd /opt/fmc_repository/Process/PythonReference/custom
ln -s /opt/fmc_repository/Telekom_Malaysia/ETSI/Python/src/ ETSI
chown -R ncuser:ncuser ETSI
```


