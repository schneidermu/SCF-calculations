# Benchmarking of the functionals on Diet GMTKN55 (30 and 50 reactions), enhancement factor calculations


## Preparing data

1) Clone the repository
2) Create and activate virtual environment, install packages from requirements.txt
3) Generate GIF-files:
```
python -m InterfaceG16 --Mode GE
```

## Calculating system energies
1) Calculate NN functionals' energies:
```
python -m InterfaceG16 --Mode CE
```

2) Calculate PBE and XAlpha energies:

```
python -m InterfaceG16 --Mode CE --Functional Non-NN
```
3) Calculate PBE0 energies and D3(BJ) corrections:
```
python -m InterfaceG16 --Mode D3
```

4) Add the D3BJ corrections to PBE and XAlpha energies (for NN functionals they are added during step 1):

```
python -m add_d3_corrections
```

5) Calculate WTMAD-2 and create a .csv table in the Results folder for comparison:
```
python -m InterfaceG16 --Functional NN_PBE > Results/NN_PBE.txt
python -m InterfaceG16 --Functional NN_XALPHA > Results/NN_XAlpha.txt
python -m InterfaceG16 --Functional PBE_D3BJ > Results/PBE-D3BJ.txt
python -m InterfaceG16 --Functional XAlpha > Results/XAlpha.txt
cd Results/
python -m txt_to_csv
```

## Enhancement factor calculations
To calculate the dependency of the enhancement factors on normed gradient, run:
```
python -m plot_exc
```

To calculate the enhancement factor in the molecule of Argon dimer, run:
```
python -m gen_cubgrid_Ar2
```

## Visualize the results
To reproduce figures with enhancement factor, run the `Fxc_Ar2_visualization.ipynb` notebook in Results folder, the .csv and .npy files are already generated in the precious steps


