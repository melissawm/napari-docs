---
theme:
  metaDescription: napari is a fast multi-dimensional image viewer for Python. It can help you **explore** any image-like data, be it 2D, 3D, or even higher-dimensional. It can also help you **overlay** downstream or **associated data**, such as point coordinates or segmentations, which you can use to **annotate** and **proofread** your image data.
---

# napari: a fast, interactive viewer for multi-dimensional images in Python

```{raw} html
<figure>

  <video width="90%" controls autoplay loop muted playsinline>
    <source src="_static/images/tribolium.webm" type="video/webm" />
    <source src="_static/images/tribolium.mp4" type="video/mp4" />
    <img src="_static/images/tribolium.jpg"
      title="your browser does not support the video tag"
      alt="napari viewer showing a 4D image of a developing Tribolium embryo.  Dataset Fluo-N3DL-TRIF from the [cell tracking challenge](http://celltrackingchallenge.net/3d-datasets/) by Dr. A. Jain, MPI-CBG, Dresden, Germany."
    >
  </video>

  <figcaption><pre>napari.imshow(image4d)</pre></figcaption>

</figure>
```

Napari is a Python library for n-dimensional image visualisation, annotation,
and analysis. With napari you can:
- **view and explore** 2D, 3D, and higher-dimensional arrays on a canvas;
- **overlay** derived data such as *points*, *polygons*, *segmentations*, and
  more;
- **annotate** and **edit** derived datasets, using standard data structures
  such as NumPy or Zarr arrays, allowing you to
- **seamlessly weave** exploration, computation, and annotation together in
  imaging data analysis.

::::{grid}

:::{grid-item-card} Examples gallery
:link: gallery
:link-type: ref

See some of the things napari can do.
:::

:::{grid-item-card} Installation
:link: napari-installation
:link-type: ref

How to install napari.
:::

:::{grid-item-card} Getting started
:link: launch
:link-type: ref

Get started with napari.
:::

::::

::::{grid}

:::{grid-item-card} Community
:link: community
:link-type: ref

Forums, web chat, video chat, and more! Join us!
:::

:::{grid-item-card} Governance
:link: napari-governance
:link-type: ref

napari is developed by a global community. See how.
:::

:::{grid-item-card} Plugins
:link: plugins-index
:link-type: ref

napari is extensible! Find plugins, or develop your own!
:::

::::
