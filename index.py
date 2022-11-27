
# import module
import streamlit as st
import pandas as pd
# Title
st.set_page_config(
	page_title = "Nanoparticles"
)
st.title("Nanomaterials Properties")


def cuboctahedral_total(layer):
	return int((10 * (layer ** 3) + 15 * (layer ** 2) + 11 * layer + 3) / 3)

def cuboctahedral_surface(layer):
	return int(10 * (layer ** 2) + 2)

def spherical_total(layer):
    return int((10 * (layer ** 3) - 15 * (layer ** 2) + 11 * layer - 3) / 3)

def spherical_surface(layer):
   	return int(10 * (layer ** 2) - 20 * layer + 12)

shape = st.radio("Select shape of nanoparticle:",('Cuboctahedral', 'Spherical'))

application = st.selectbox("Select an application:",('Optical', 'Electrical', 'Magnetic', 'Strength', 'None'), 4)

global max_range, min_range
if(application=='Optical'):
	min_range=40; max_range=100
elif(application=='Electrical'):
	min_range=10; max_range=20
elif(application=='Magnetic'):
	min_range=1; max_range=10
elif(application=='Strength'):
	min_range=1; max_range=50
else:
	min_range=1; max_range=50

values = st.slider('Specify size limits for nanoparticle: (in nm)', min_range, max_range, (min_range, max_range))

sizes = [i for i in range(values[0], values[1]+1)]
atoms_surface = []
atoms_bulk = []
atom_data = []

if(shape=='Cuboctahedral'):
	atom_data = [[i,int(cuboctahedral_total(i)-cuboctahedral_surface(i)),cuboctahedral_surface(i), cuboctahedral_total(i)] for i in sizes]
	atoms_surface = [(cuboctahedral_surface(k)/cuboctahedral_total(k))*100 for k in sizes]
	atoms_bulk = [(1-(cuboctahedral_surface(k)/cuboctahedral_total(k)))*100 for k in sizes]
elif(shape=='Spherical'):
	atom_data = [[i,int(spherical_total(i)-spherical_surface(i)),spherical_surface(i), spherical_total(i)] for i in sizes]
	atoms_surface = [(spherical_surface(k)/spherical_total(k))*100 for k in sizes]
	atoms_bulk = [(1-(spherical_surface(k)/spherical_total(k)))*100 for k in sizes]

percentages = [[atoms_surface[i], atoms_bulk[i]] for i in range(len(sizes))]
ratios = [atoms_bulk[i]/atoms_surface[i]*100 for i in range(len(sizes))]

atoms_df = pd.DataFrame(atom_data[:5], columns = ['Particle Size','Bulk atoms', 'Surface atoms', 'Total atoms'])
st.table(atoms_df)

chart_data = pd.DataFrame(percentages, columns=['Surface atoms', 'Bulk atoms'])
ratio_data = pd.DataFrame(ratios)

if st.button('Plot graphs'):
	st.write("% of Bulk and Surface atoms vs. Particle Size")
	st.line_chart(chart_data)
	st.write("Ratio of bulk/surface atoms vs. Particle Size")
	st.line_chart(ratio_data)