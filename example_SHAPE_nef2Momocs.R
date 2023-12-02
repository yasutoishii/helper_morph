library(Momocs)

outcoe.obj = OutCoe(
  read.csv(
    "Outputed_file_from_SHAPE_nef2Momocs.py",
    header=T,
    row.names=1
  ),
  method = "efourier",
  norm = "dummy"
)

Momocs::PCA(outcoe.obj)
PCcontrib(outcoe.obj, nax = 1:4)

