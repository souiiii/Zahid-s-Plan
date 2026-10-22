# Revision notes

AI-maintained starter cards derived from the linked NCERT chapters. They are compact retrieval aids, not a substitute for the chapter. Personal errors are empty until reported. Read the prompt and recall first; check the card afterward.

## Relations & Functions

Recall: State the three equivalence conditions, then outline a one–one/onto proof.

- Reflexive: every (a,a) belongs to R. Symmetric: (a,b) implies (b,a). Transitive: (a,b) and (b,c) imply (a,c). Equivalence needs all three.
- One–one: f(a)=f(b) forces a=b. Onto: every element of the stated codomain has a preimage; check restrictions on both domain and codomain.
- For a failure, give a concrete counterexample. For onto, solve y=f(x) for x and verify that x is allowed.

Source: [lemh101.pdf](../Sources/Books/maths-part-1/lemh101.pdf)

Personal corrections: none recorded yet.

## Inverse Trigonometric Functions

Recall: Write the principal ranges without notes and explain one branch restriction.

- Principal ranges: arcsin x in [−π/2,π/2]; arccos x in [0,π]; arctan x in (−π/2,π/2).
- Principal ranges: arccot x in (0,π); arcsec x in [0,π] except π/2; arccosec x in [−π/2,π/2] except 0.
- Domains: arcsin/arccos need |x|≤1; arcsec/arccosec need |x|≥1. Simplifications must respect the principal branch.
- sin⁻¹(sin θ)=θ only when θ is in the principal range. Do not cancel inverse symbols without checking the interval.

Source: [lemh102.pdf](../Sources/Books/maths-part-1/lemh102.pdf)

Personal corrections: none recorded yet.

## Matrices

Recall: Explain the order of AB, and reproduce the transpose-of-product rule.

- AB exists when columns(A)=rows(B). Multiplication is generally noncommutative.
- (AB)ᵀ=BᵀAᵀ. Symmetric: Aᵀ=A. Skew-symmetric: Aᵀ=−A, so each real diagonal entry is zero.
- For invertible A: A⁻¹A=AA⁻¹=I; (AB)⁻¹=B⁻¹A⁻¹ when both inverses exist.

Source: [lemh103.pdf](../Sources/Books/maths-part-1/lemh103.pdf)

Personal corrections: none recorded yet.

## Determinants

Recall: Write the inverse criterion and explain how cofactors form the adjoint.

- For a 2×2 matrix, determinant ad−bc. Cofactor Cij=(−1)^(i+j)×minor Mij; adj(A) is the transpose of the cofactor matrix.
- A⁻¹=adj(A)/|A| only if |A|≠0. Solve AX=B as X=A⁻¹B when A is invertible.
- Swapping two rows changes determinant sign; a row multiple scales the determinant; adding a multiple of another row leaves it unchanged.
- In a board calculation, keep the cofactor signs visible and check the proposed solution by substitution.

Source: [lemh104.pdf](../Sources/Books/maths-part-1/lemh104.pdf)

Personal corrections: none recorded yet.

## Electric Charges & Fields

Recall: State Gauss’s law and distinguish line, plane-sheet and shell fields.

- Coulomb: F=(1/4πε₀)q₁q₂/r² in magnitude with the appropriate force direction. Add fields as vectors.
- Flux through a closed surface: ∮E·dA=Qenclosed/ε₀. The enclosed charge controls net flux, not necessarily the field at each point.
- Infinite line: E=λ/(2πε₀r). Infinite nonconducting plane sheet: E=σ/(2ε₀). Thin spherical shell: E=0 inside and kQ/r² outside.
- Electric dipole moment points from negative to positive charge. Torque τ=p×E; draw the geometry before using components.

Source: [leph101.pdf](../Sources/Books/phy-part-1/leph101.pdf)

Personal corrections: none recorded yet.

## Potential & Capacitance

Recall: Explain connected versus disconnected capacitor changes before writing a formula.

- Point-charge potential V=kq/r; potentials add algebraically. Along x, Eₓ=−dV/dx.
- C=Q/V. Parallel plate: C=ε₀A/d; full dielectric: C=Kε₀A/d. Parallel capacitances add; series reciprocals add.
- Energy U=Q²/(2C)=CV²/2=QV/2. Battery disconnected means fixed Q; battery connected means fixed V.
- For a dielectric change, identify fixed Q or fixed V first, then calculate C, V and U. Equipotentials have E perpendicular to the surface.

Source: [leph102.pdf](../Sources/Books/phy-part-1/leph102.pdf)

Personal corrections: none recorded yet.

## Continuity & Differentiability

Recall: Write the continuity test, chain rule and correct parametric second derivative.

- Continuity at a requires LHL=RHL=f(a). For piecewise functions, check every join and the actual value at the join.
- Differentiable implies continuous; continuous does not imply differentiable. At a suspected corner, compare the one-sided derivatives.
- Chain rule: d f(g(x))/dx=f′(g(x))g′(x). Implicit differentiation: differentiate y as a function of x and collect dy/dx.
- d(ln x)/dx=1/x for x>0; d(eˣ)/dx=eˣ; d(aˣ)/dx=aˣ ln a. For variable powers y=u(x)^v(x), take logs on the domain u>0.
- For x=x(t), y=y(t): dy/dx=(dy/dt)/(dx/dt); d²y/dx²=[d(dy/dx)/dt]/(dx/dt) where the denominator is nonzero.

Source: [lemh105.pdf](../Sources/Books/maths-part-1/lemh105.pdf)

Personal corrections: none recorded yet.

## Current Electricity

Recall: Derive I=neAvd, explain a terminal-voltage sign and state the bridge condition.

- I=neAvd in magnitude. Mobility μ=vd/E. Conductivity σ=neμ; resistivity ρ=1/σ and R=ρL/A.
- Near a reference temperature, R=R₀[1+α(T−T₀)] when the linear approximation applies. Power P=VI=I²R=V²/R for a resistor.
- Discharging cell: terminal V=ε−Ir; charging cell: V=ε+Ir under the stated current direction.
- Series-aiding cells: εeq=ε₁+ε₂, req=r₁+r₂. Parallel like-polarity cells: εeq=(ε₁/r₁+ε₂/r₂)/(1/r₁+1/r₂), req=r₁r₂/(r₁+r₂).
- Kirchhoff: charge conservation at a junction; energy conservation around a loop. Draw assumed directions first. For a balanced Wheatstone bridge, the galvanometer current is zero and corresponding arm ratios are equal.

Source: [leph103.pdf](../Sources/Books/phy-part-1/leph103.pdf)

Personal corrections: none recorded yet.

## Solutions

Recall: Recall concentration denominators, Henry/Raoult and which way association changes i.

- Molarity: moles of solute/litres of solution. Molality: moles of solute/kg of solvent. Mole fraction: ni/Σnj. State which mass or volume is the denominator.
- Henry: p=KH x at a given temperature. Raoult for an ideal volatile component: pi=xi pi°. For two volatile components, total pressure is the sum.
- Weaker A–B interactions generally cause positive deviation; stronger A–B interactions cause negative deviation. An azeotrope has the same liquid/vapour composition at its boiling point.
- ΔTb=iKb m; ΔTf=iKf m; π=iCRT. Use kelvin and consistent units. Relative vapour-pressure lowering equals solute mole fraction for an ideal solution with a nonvolatile solute.
- Association decreases particle count (i<1); dissociation increases it (i>1). For dissociation into ν particles: i=1+α(ν−1). For n-mers formed by association: i=1−α(1−1/n).

Source: [lech101.pdf](../Sources/Books/chem-part-1/lech101.pdf)

Personal corrections: none recorded yet.

## Organic foundation

Recall: Identify the attacking species, electron-deficient atom and direction of the electron-pair arrow.

- Read structures by satisfying carbon valency four. Name a parent chain containing the principal functional group before assigning substituents.
- Nucleophiles donate an electron pair; electrophiles accept it. Curved full arrows begin at an electron pair or bond, not at a bare positive charge.
- Heterolytic fission allocates both bond electrons to one atom; homolytic fission allocates one to each. Formal cleavage drawings do not establish an actual reaction pathway.
- Inductive effects travel through sigma bonds and weaken with distance. Resonance moves electrons through a conjugated system; atoms do not move between contributors.
- Compare acid strength by stability of conjugate bases. Recognise substitution, elimination, addition and oxidation/reduction before learning chapter-specific mechanisms.

Source: [kech202.pdf](../Sources/Books/chem-class-11-bridge/kech202.pdf)

Personal corrections: none recorded yet.
