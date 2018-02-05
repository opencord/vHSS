# Virtual Home Subscriber Server Service (vHSS) for 5.0

## Onboarding

To onboard this service in your system, you can add the service to the `mcord.yml` profile manifest (location: $CORD/build/platform-install/profile_manifests/mcord.yml):

```
xos_services:
  - name: vhss
    path: orchestration/xos_services/vhss
    keypair: mcord_rsa
```

In addition, you should add the synchronizer for this service to the `docker_images.yml` (location: $CORD/build/docker_images.yml):

```
  - name: xosproject/vhss-synchronizer
    repo: vHSS
    path: "xos/synchronizer"
    dockerfile: "Dockerfile.synchronizer"
```

To build the synchronizer as a container, following codes should be written in scenario files, e.g., cord, local, mock, and so on:

```
docker_image_whitelist:
  - "xosproject/vhss-synchronizer"
```

For this, the exact location for each scenario is as follows:
 - for CORD scenario: $CROD/build/scenarios/cord/config.yml
 - for Local scenario: $CROD/build/scenarios/local/config.yml
 - for Mock scenario: $CROD/build/scenarios/mock/config.yml
 - for Opencloud scenario: $CROD/build/scenarios/opencloud/config.yml
 - for Single scenario: $CROD/build/scenarios/single/config.yml

Once you have added the service, you will need to rebuild and redeploy the XOS containers from source.

```
$ cd $CORD/build
$ make xos-teardown
$ make clean-openstack
$ make clean-profile
$ make -j4 build
$ make compute-node-refresh
```
