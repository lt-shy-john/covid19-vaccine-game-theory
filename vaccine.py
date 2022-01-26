class Vaccine:

    def __init__(self, name='Sample', dose=0, days=0, vaccine_type=0, cost=0, efficacy=0, alpha=0, beta=0, gamma=0, delta=0, phi=0):
        self.brand = name
        self.dose = dose
        self.days_to_next_dose = days
        self.type = vaccine_type
        self.cost = cost
        self.efficacy = efficacy
        self.alpha_V = alpha
        self.beta_V = beta
        self.gamma_V = gamma
        self.delta_V = delta
        self.phi_V = phi
        self.next = None # Next dose
