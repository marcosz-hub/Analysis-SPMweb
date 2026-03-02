#####################################################################################
# Path analysis from SPMweb
#####################################################################################

#Importar librerias

import re # Recons repetitive sintaxis
import pandas as pd #Manages dataframe for excel


# Functions

def procesar_pml(archivo_entrada, nombre_salida):
    dict_radios = {}
    filas_enlaces = []

    try:
        with open(archivo_entrada, "r", encoding="utf-8") as f:
            lineas = f.readlines()

        # Step 1: Search spheres radios
        for linea in lineas:
            buscar_bola = re.search(r"set sphere_scale,([\d\.]+).*resi (\d+)", linea)
            if buscar_bola:
                size_ = float(buscar_bola.group(1))
                id_resi = int(buscar_bola.group(2)) 
                dict_radios[id_resi] = size_

        # Step 2: Search for resi in bonds
        resi1, resi2 = None, None
        for linea in lineas:
            buscar_enlace = re.search(r"bond name ca and resi (\d+), name ca and resi (\d+)", linea)            
            if buscar_enlace:
                resi1 = int(buscar_enlace.group(1))
                resi2 = int(buscar_enlace.group(2))

            # Search for stick_radius 
            buscar_stick = re.search(r"set stick_radius,([\d\.]+)", linea)
            if buscar_stick and resi1 is not None:
                size_stick = float(buscar_stick.group(1))
                
                
                radio_1 = dict_radios.get(resi1, 0.0)
                radio_2 = dict_radios.get(resi2, 0.0)

                filas_enlaces.append({
                    "Residue_1": resi1,
                    "Sphere_Radius_1": radio_1,
                    "Residue_2": resi2,
                    "Sphere_Radius_2": radio_2,
                    "Stick_Radius": size_stick
                })
                # Reset temporal variables
                resi1, resi2 = None, None

        if not filas_enlaces:
            print(f"⚠️ Data not valid in {archivo_entrada}")
            return

        # Step 3: Export dataframe
        df = pd.DataFrame(filas_enlaces)
        df = df.sort_values("Residue_1") 

        if not nombre_salida.lower().endswith('.xlsx'):
            nombre_salida += ".xlsx"
            
        df.to_excel(nombre_salida, index=False)
        print(f"✅ Script finished succsesfully. File created: {nombre_salida}")

    except FileNotFoundError:
        print(f"❌ Error: Input file '{archivo_entrada}' does not exist.")
    except Exception as e:
        print(f"❌ An error ocurred: {e}")

# --- User interface ---
while True:
    print("\n--- Path analysis from SPMweb ---")

    #Input file name
    archivo_in = input("1. Name of the input file (.pml/.txt) or exit (exit, quit, q): ")
    
    if archivo_in.lower() in ['exit', 'quit', 'q']: 
        break
    
    #Name of the output file
    archivo_out = input("2. Name of output file (.xlsx): ")
    
    procesar_pml(archivo_in, archivo_out)