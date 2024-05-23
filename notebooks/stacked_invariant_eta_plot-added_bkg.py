import ROOT

def create_lorentz_vector(pt, eta, phi, mass):
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(pt, eta, phi, mass)
    return lv

def process_file(file_path, tree_name):
    file = ROOT.TFile(file_path, "READ")
    tree = file.Get(tree_name)

    invariant_etas = []

    if not tree:
        print(f"Tree not found in file: {file_path}")
    else:
        for event in tree:
            lead_pt = event.lead_pt
            lead_eta = event.lead_eta
            lead_phi = event.lead_phi
            lead_energyRaw = event.lead_energyRaw

            sublead_pt = event.sublead_pt
            sublead_eta = event.sublead_eta
            sublead_phi = event.sublead_phi
            sublead_energyRaw = event.sublead_energyRaw

            # Calculate the invariant eta
            lv1 = create_lorentz_vector(lead_pt, lead_eta, lead_phi, lead_energyRaw)
            lv2 = create_lorentz_vector(sublead_pt, sublead_eta, sublead_phi, sublead_energyRaw)
            invariant_eta = (lv1 + lv2).Eta()

            invariant_etas.append(invariant_eta)

    file.Close()
    return invariant_etas

# File paths
data_file_paths = ["../output_root/Data_EraE.root", "../output_root/Data_EraF.root", "../output_root/Data_EraG.root"]
background_files = [
    ("../output_root/GGJets.root", "#gamma#gamma+jets"),
    ("../output_root/GJetPt20To40.root", "#gamma+jets with 20 < P_{T} < 40"),
    ("../output_root/GJetPt40.root", "#gamma+jets with P_{T} > 40"),
#     ("../output_root/GluGluHToGG.root", "H#rightarrow#gamma#gamma"),
#     ("../output_root/ttHToGG.root", "H#rightarrow#gamma#gamma"),
#     ("../output_root/VBFHToGG.root", "H#rightarrow#gamma#gamma"),
#     ("../output_root/VHToGG.root", "H#rightarrow#gamma#gamma")
]

# Tree and variable names
tree_name = "DiphotonTree/data_125_13TeV_NOTAG"

# Process data files
data_invariant_etas = []
signal_etas = []
for data_file_path in data_file_paths:
    data_invariant_etas.extend(process_file(data_file_path, tree_name))

    # Process signal variables from data files
    file = ROOT.TFile(data_file_path, "READ")
    tree = file.Get(tree_name)

    if tree:
        for event in tree:
            pt = event.HHbbggCandidate_pt
            eta = event.HHbbggCandidate_eta
            phi = event.HHbbggCandidate_phi
            mass = event.HHbbggCandidate_mass

            lv_signal = create_lorentz_vector(pt, eta, phi, mass)
            signal_etas.append(lv_signal.Eta())

    file.Close()

# Process background files
background_hists = {}
background_colors = [ROOT.kBlue-9, ROOT.kOrange-2, ROOT.kYellow-7, ROOT.kGreen-7, ROOT.kCyan-7, ROOT.kMagenta-7, ROOT.kViolet-7]

for i, (background_file, bg_name) in enumerate(background_files):
    bg_invariant_etas = process_file(background_file, tree_name)
    bg_hist = ROOT.TH1F(f"hist_{bg_name}", f"{bg_name} Invariant Eta", 40, -5, 5)  # Adjust the binning as needed
    for eta in bg_invariant_etas:
        bg_hist.Fill(eta)
    if i < len(background_colors):
        bg_hist.SetFillColor(background_colors[i])
    else:
        # If there are more background files than colors, loop back to the start of the colors list
        bg_hist.SetFillColor(background_colors[i % len(background_colors)])
    background_hists[bg_name] = bg_hist

# Combine all backgrounds into a single histogram
total_background_hist = None
for bg_hist in background_hists.values():
    if total_background_hist is None:
        total_background_hist = bg_hist.Clone()
    else:
        total_background_hist.Add(bg_hist)

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
stack = ROOT.THStack("stack", "")
for bg_name, bg_hist in background_hists.items():
    stack.Add(bg_hist)
stack.Draw("HIST")

# Draw the data
data_hist = ROOT.TH1F("data_hist", "Data Invariant Eta", 40, -5, 5)
for eta in data_invariant_etas:
    data_hist.Fill(eta)
data_hist.SetMarkerStyle(20)
data_hist.SetMarkerSize(1)
data_hist.Draw("SAME E1")

# Draw the signal
signal_hist = ROOT.TH1F("signal_hist", "Signal Invariant Eta", 40, -5, 5)
for eta in signal_etas:
    signal_hist.Fill(eta)
signal_hist.SetLineColor(ROOT.kRed)
signal_hist.SetLineWidth(2)
signal_hist.Draw("SAME HIST")

# Add legend
legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
legend.AddEntry(data_hist, "Data", "lep")
legend.AddEntry(signal_hist, "Signal", "l")
for bg_name, bg_hist in background_hists.items():
    legend.AddEntry(bg_hist, bg_name, "f")
legend.Draw()

# Set y-axis range for the main plot
stack.SetMinimum(0)
stack.SetMaximum(30000)

# Set y-axis title
stack.GetYaxis().SetTitle("Events")

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

# Ratio plot
canvas.cd()
pad2 = ROOT.TPad("pad2", "Ratio Plot", 0, 0, 1, 0.3)
pad2.SetTopMargin(0.05)
pad2.SetBottomMargin(0.3)
pad2.SetTicks(1, 1)
pad2.Draw()
pad2.cd()

ratio_hist = data_hist.Clone("ratio_hist")
ratio_hist.Divide(total_background_hist)
ratio_hist.SetMarkerStyle(20)
ratio_hist.SetMarkerSize(1)
ratio_hist.SetStats(0)
ratio_hist.SetTitle("")
ratio_hist.GetYaxis().SetTitle("Data/MC")
ratio_hist.GetYaxis().SetTitleSize(0.1)
ratio_hist.GetYaxis().SetTitleOffset(0.5)
ratio_hist.GetYaxis().SetLabelSize(0.08)
ratio_hist.GetXaxis().SetTitle("#eta_{#gamma#gamma}")
ratio_hist.GetXaxis().SetTitleSize(0.12)
ratio_hist.GetXaxis().SetTitleOffset(0.9)
ratio_hist.GetXaxis().SetLabelSize(0.08)
ratio_hist.GetYaxis().SetRangeUser(0, 4)  # Adjusted range for the ratio plot
ratio_hist.Draw("E1")

# Draw horizontal lines at y=1, y=2, y=3
for y in range(0, 4):
    line = ROOT.TLine(ratio_hist.GetXaxis().GetXmin(), y, ratio_hist.GetXaxis().GetXmax(), y)
    line.SetLineStyle(2)  # Dashed line
    line.SetLineColor(ROOT.kRed)
    line.Draw()

# Save the canvas as a PDF file
canvas.Print("/afs/cern.ch/user/s/sraj/sraj/www/CUA/HH-bbgg/invariant_eta_plot_with_signal_Without_hgg.pdf")

# Show the canvas
canvas.Draw()
