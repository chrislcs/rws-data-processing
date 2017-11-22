# Build Cesium point cloud tiles using Entwine

Create point cloud cesium 3D tiles using Entwine.

## Usage

Install [Entwine](https://github.com/connormanning/entwine) (requires [PDAL](https://www.pdal.io/)).

The easiest way to get Entwine running is by using [Docker](http://docker.com/).

- Download and install Docker
- Go to Docker settings and share the drive containing the data and config files.
- Open a command prompt
- Pull the Entwine Docker image by entering the following command:

    `docker pull connormanning/entwine`

- Copy the `entwine-cesium-config.json` file into the input data folder
- Generate the Cesium point cloud tiles by entering the following command (replacing \*path to input folder\* with the path to the folder containing the las/laz files):

    `docker run -it -v *path to input folder*:/data/ connormanning/entwine build /data/entwine-cesium-config.json -i /data/ -o /data/output/`

NB: Make sure the docker instance has enough memory allocated. If not enough memory is available the process might get cut off before it is finished. You can set the amount of memory in the docker settings under the `advanced` tab.