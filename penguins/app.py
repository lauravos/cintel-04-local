import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly, output_widget, render_widget
from shiny import render, App, reactive
import palmerpenguins # import the Palmer Penguin dataset
import seaborn as sns


# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Gagnon-Vos Penguin Data", fillable=True)

# Add a Shiny UI sidebar for user interaction

with ui.sidebar(open = "open"):
    ui.h2("Sidebar")

# Use ui.input_selectize() to create a dropdown input to choose a column
    
    ui.input_selectize("selectized_attribute", "Select Attribute", ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

# Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins

    ui.input_numeric("plotly_bin_count", "Bin Count", 10, min=1, max=20)

# Use ui.input_slider() to create a slider input for the number of Seaborn bins

    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 0, 100, 50)

# Use ui.input_checkbox_group() to create a checkbox group input to filter the species

    ui.input_checkbox_group("selected_species_list", "Species", ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie", "Gentoo", "Chinstrap"], inline=False)

#Create a checkbox group input to filter the species
    ui.input_checkbox_group("island_list", "Island", ["Torgersen", "Biscoe", "Dream"], selected=["Torgersen", "Biscoe", "Dream"], inline=False)

# Use ui.hr() to add a horizontal rule to the sidebar

    ui.hr()

# Use ui.a() to add a hyperlink to the sidebar

    ui.a("Github", href="https://github.com/lauravos/cintel-02-data", target="_blank")


#DataTable
with ui.navset_card_tab(id="tab"):
    with ui.nav_panel("Data Table"):
        @render.data_frame  
        def penguins_dataTable():
            return render.DataTable(filtered_data())  

#DataGrid
    with ui.nav_panel("Data Grid"):
        ui.h2("Palmer Penguins")
        @render.data_frame  
        def penguins_dataGrid():
            return render.DataGrid(filtered_data())  


#Plotly Histogram
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Plotly Histogram"):   

        @render_widget  
        def plotly():  
            scatterplot = px.histogram(
                data_frame=filtered_data(),
                x=input.selectized_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            ).update_layout(
                title={"text": "Plotly Histogram", "x": 0.5},
                yaxis_title="Count",
                xaxis_title=input.selectized_attribute()
            )

            return scatterplot  


#Seaborn Histogram
    with ui.accordion_panel("Seaborn Histogram"):

        @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")  
        def plotHistogram():  
            ax = sns.histplot(data=filtered_data(), x=input.selectized_attribute(), bins=input.seaborn_bin_count())  
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selectized_attribute())
            ax.set_ylabel("Count")
            return ax  


#Plotly Scatterplot

with ui.card(full_screen=True):

    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        # Create a Plotly scatterplot using Plotly Express
        # Call px.scatter() function
        # Pass in six arguments:
        fig = px.scatter(filtered_data(), x=input.selectized_attribute(), y="body_mass_g", 
                         color="species", title="Scatterplot",labels={"bill_length_mm": "Bill Length (mm)", "bill_depth_mm": "Bill Depth (mm)", "flipper_length_mm": "Flipper Length (mm)",
                         "body_mass_g": "Body Mass (g)"})
        return fig

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    isSpeciesMatch = penguins_df["species"].isin(input.selected_species_list()) & penguins_df["island"].isin(input.island_list())
    return penguins_df[isSpeciesMatch]
