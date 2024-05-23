import ROOT
import json



@lorentz_vector
def create_lorentz_vector(pt, eta, phi, mass):
    lv = ROOT.TLorentzVector()
    lv.SetPtEtaPhiM(pt, eta, phi, mass)
    return lv


@file_processing
def process_file(file_path, tree_name):
    file = ROOT.TFile(file_path, "READ")
    tree = file.Get(tree_name)

    invariant_etas = []
    invariant_masses = []

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

            lv1 = create_lorentz_vector(lead_pt, lead_eta, lead_phi, lead_energyRaw)
            lv2 = create_lorentz_vector(sublead_pt, sublead_eta, sublead_phi, sublead_energyRaw)
            invariant_eta = (lv1 + lv2).Eta()
            invariant_mass = (lv1 + lv2).M()

            invariant_etas.append(invariant_eta)
            invariant_masses.append(invariant_mass)

    file.Close()
    return invariant_etas, invariant_masses





@CMS_Style

def create_cms_style():
    # Create a canvas
    canvas = ROOT.TCanvas("canvas", "Invariant Eta", 800, 800)

    # Divide the canvas into two pads, one for the main plot and one for the ratio plot
    pad1 = ROOT.TPad("pad1", "Main Plot", 0, 0.3, 1, 1)
    pad1.SetBottomMargin(0.02)
    pad1.SetTopMargin(0.1)
    pad1.SetTicks(1, 1)
    pad1.Draw()
    pad1.cd()

    # Create legend
    legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)

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

    return canvas, pad1, legend
