import ROOT

def create_lorentz_vector(pt, eta, phi, mass):
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(pt, eta, phi, mass)
    return lv

def process_file(file_path, tree_name, variables):
    file = ROOT.TFile(file_path, "READ")
    tree = file.Get(tree_name)

    values = {var[0]: [] for var in variables}

    if not tree:
        print(f"Tree not found in file: {file_path}")
    else:
        for event in tree:
            for var, suffix in variables:
                value = getattr(event, var + suffix)
                values[var].append(value)

    file.Close()
    return values


def plot_stacked_hist(file_paths, background_files, tree_name, variables, output_file):
    # Process data files
    data_values = {var: [] for var in variables}
    for data_file_path in file_paths:
        values = process_file(data_file_path, tree_name, variables)
        for var, var_values in values.items():
            data_values[var].extend(var_values)

    # Process background files
    background_hists = {}
    background_colors = [ROOT.kBlue-9, ROOT.kOrange-2, ROOT.kYellow-7, ROOT.kGreen-7, ROOT.kCyan-7, ROOT.kMagenta-7, ROOT.kViolet-7]

    for i, (background_file, bg_name) in enumerate(background_files):
        bg_values = process_file(background_file, tree_name, variables)
        for var, var_values in bg_values.items():
            bg_hist = ROOT.TH1F(f"hist_{bg_name}_{var}", f"{bg_name} {var}", 40, -5, 5)  # Adjust the binning as needed
            for value in var_values:
                bg_hist.Fill(value)
            if i < len(background_colors):
                bg_hist.SetFillColor(background_colors[i])
            else:
                # If there are more background files than colors, loop back to the start of the colors list
                bg_hist.SetFillColor(background_colors[i % len(background_colors)])
            background_hists[(bg_name, var)] = bg_hist

    # Combine all backgrounds into a single histogram
    total_background_hists = {}
    for bg_name, var in variables:
        total_background_hist = None
        for bg_hist in background_hists.values():
            if bg_name in bg_hist.GetName() and var in bg_hist.GetName():
                if total_background_hist is None:
                    total_background_hist = bg_hist.Clone()
                else:
                    total_background_hist.Add(bg_hist)
        total_background_hists[(bg_name, var)] = total_background_hist

    # Create a canvas
    canvas = ROOT.TCanvas("canvas", "Invariant Eta", 800, 800)

    # Divide the canvas into two pads, one for the main plot and one for the ratio plot
    pad1 = ROOT.TPad("pad1", "Main Plot", 0, 0.3, 1, 1)
    pad1.SetBottomMargin(0.02)
    pad1.SetTopMargin(0.1)
    pad1.SetTicks(1, 1)
    pad1.Draw()
    pad1.cd()

    # Draw the stack of backgrounds
    stack = {}
    for var in variables:
        stack[var] = ROOT.THStack(f"stack_{var}", "")
        for bg_name, bg_hist in total_background_hists.items():
            if var in bg_name:
                stack[var].Add(bg_hist)
        stack[var].Draw("HIST")

    # Draw the data
    data_hists = {}
    for var in variables:
        data_hists[var] = ROOT.TH1F(f"data_hist_{var}", f"Data {var}", 40, -5, 5)
        for value in data_values[var]:
            data_hists[var].Fill(value)
        data_hists[var].SetMarkerStyle(20)
        data_hists[var].SetMarkerSize(1)
        data_hists[var].Draw("SAME E1")

    # Add legend
    legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
    for var in variables:
        legend.AddEntry(data_hists[var], f"Data {var}", "lep")
        for bg_name, bg_hist in background_hists.items():
            if var in bg_name:
                legend.AddEntry(bg_hist, bg_name, "f")
    legend.Draw()

    # Set y-axis range for the main plot
    for var in variables:
        stack[var].SetMinimum(0)
        stack[var].SetMaximum(30000)  # Adjust as needed

    # Set y-axis title
    for var in variables:
        stack[var].GetYaxis().SetTitle("Events")

    # Add CMS text
    cms_label = ROOT.TLatex()
    cms_label.SetNDC()
    cms_label.SetTextFont(61)
    cms_label.SetTextSize(0.04)
    cms_label.DrawLatex(0.1, 0.91, "CMS")

    # Add "Work in Progress"
    work_label = ROOT.TLatex()
    work_label.SetNDC()
    work_label.SetTextFont(52)
    work_label.SetTextSize(0.03)
    work_label.DrawLatex(0.16, 0.91, "Work in Progress")

    # Add energy information
    energy_label = ROOT.TLatex()
    energy_label.SetNDC()
    energy_label.SetTextFont(42)
    energy_label.SetTextSize(0.03)
    energy_label.DrawLatex(0.83, 0.91, "(13.6 TeV)")

    # Save the canvas as a PDF file
    canvas.Print(output_file)

    # Show the canvas
    canvas.Draw()

# Example usage
data_file_paths = ["../output_root/Data_EraE.root", "../output_root/Data_EraF.root", "../output_root/Data_EraG.root"]
background_files = [
    ("../output_root/GGJets.root", "#gamma#gamma+jets"),
    ("../output_root/GJetPt20To40.root", "#gamma+jets with 20 < P_{T} < 40"),
    ("../output_root/GJetPt40.root", "#gamma+jets with P_{T} > 40"),
]
tree_name = "DiphotonTree/data_125_13TeV_NOTAG"
variables = [("lead_eta", ""), ("sublead_eta", "")]
output_file = "stacked_plot.pdf"

plot_stacked_hist(data_file_paths, background_files, tree_name, variables, output_file)

