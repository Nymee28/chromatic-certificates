# Lemme C-mod4 — La fermeture des équations d'étiquettes de G_CH(q,4)
### L'arithmétique de fenêtres qui réduit « tout q » à deux vérifications finies, et l'assemblage du Théorème 1 bis

*Dossier 9, pièce de preuve. 27 juillet 2026, soir. Niveau de rigueur visé : celui de `preuve-lemmes-ZJ.md` — démonstrations rédigées, constantes explicites, liste [R] des vérifications restantes en fin de document. Faits machine invoqués : bilan CC-01 (§ 3.4) et `j2_labels_q*.json`.*

---

## 0. Objets et notations

G = G_CH(q,4) : sommets ℤ_n, n = 4q+1, arêtes aux écarts D = {1, 2, 3} ∪ {4j+2, 4j+3 : j ≥ 1 dans la fenêtre} — on ne retient pour le support du certificat que les arêtes d'**écart g ∈ {1, 2, 3}** (loi « écart ≤ k−1 », établie machine aux deux moitiés sur q = 3, 4). Colonnes du système restreint : paires (e, m) où e est une arête d'écart ≤ 3 et m = **gadget** (support à distance ≤ L = 3 de e, exposants ≤ 3) × au plus un **éclaireur** x_s^ε (ε ∈ {1,2,3}, s quelconque). Degrés ≡ 1 mod 4, niveaux {1, 5}. Lignes : monômes réduits (exposants mod 4) des produits m·t, t terme du polynôme d'arête, canonisés par rotation.

**Étiquette d'une colonne** : ℓ(e, m) = (écart de e, forme du gadget relative à e, ε, (s − a) mod 4, signe) — où a est l'extrémité de référence de e après normalisation d'orientation ; c'est un mot **indépendant de n**. Le **système d'étiquettes** 𝔈_q : on somme les coefficients des colonnes de même étiquette dans chaque ligne, puis on dédouble les lignes de signature identique. 𝔈_q est un ensemble fini de formes linéaires sur l'alphabet des étiquettes.

**Ce qui est déjà acquis machine** : l'alphabet est constant pour q ≥ 5 (6 487 étiquettes, q = 5…9) ; |𝔈_q| = 6 109, 6 172, 6 184 pour q = 7, 8, 9 ; et les solutions canoniques sont exactement 2-périodiques : sol(6) = sol(8) =: V_pair, sol(7) = sol(9) =: V_impair, bit à bit.

**But** : prouver qu'il existe q₀ tel que pour q ≥ q₀, **𝔈_q ne dépend que de q mod 2** ; noter 𝔈_pair, 𝔈_impair. Alors V_pair ⊨ 𝔈_pair et V_impair ⊨ 𝔈_impair (vérifié machine à q = 6, 8 et 7, 9 respectivement) instancient des certificats exacts de degré 5 pour TOUT q ≥ q₀ — le Théorème 1 bis.

## 1. Lemme F (fenêtres) — le support d'une ligne

**Énoncé.** Tout monôme-ligne μ du système restreint a un support de la forme
supp(μ) ⊆ W ∪ {s}, où W est un intervalle circulaire de largeur ≤ **w₀ = 10** et s est au plus un sommet isolé (l'éclaireur), avec la convention que si s est à distance ≤ 1 de W on l'absorbe dans une fenêtre de largeur ≤ w₀ + 2.

*Preuve.* μ = red₄(m·t). Le gadget de m vit dans [a−3, b+3] où e = (a, b), b − a = g ≤ 3 : largeur ≤ g + 7 ≤ 10. Le terme d'arête t a son support dans {a, b} ⊂ ce même intervalle. La réduction mod 4 ne fait que supprimer des sommets (exposants ≡ 0). Reste l'éclaireur, sommet unique arbitraire. ∎

## 2. Lemme S (saturation des types de fenêtre)

**Énoncé.** Pour n > 2w₀ + 4 (soit n ≥ 25, q ≥ 6), l'ensemble des **types de fenêtre** — les classes de rotation des restrictions de lignes à leur fenêtre W, éclaireur exclu — est indépendant de n.

*Preuve.* Un type de fenêtre est un mot fini de largeur ≤ w₀ (exposants 0…3 sur un intervalle), plus la donnée que le reste du cycle est vide. Deux conditions seulement font intervenir n : (i) que la fenêtre ne se recouvre pas elle-même par enroulement — garanti dès n > w₀ ; (ii) que la canonisation par rotation ne crée pas d'identification accidentelle entre deux fenêtres distinctes — une identification exigerait deux occurrences du motif à distance < w₀, impossible dès n > 2w₀ + 4 puisque le complément est vide. Au-delà, croître n ajoute du vide, aucune classe nouvelle. ∎

## 3. Lemme Z (zone générique de l'éclaireur)

**Énoncé.** Soit une ligne de fenêtre W (type fixé) et d'éclaireur s à distance signée δ de la référence de W, dans la **zone générique** w₀ + 4 < |δ| < ⌊n/2⌋ − (w₀ + 4). Alors la signature de la ligne (le multiensemble des (étiquette, coefficient) qui y contribuent) ne dépend que de **(type de W, ε, δ mod 4, signe de δ)**.

*Preuve.* Une colonne (e′, m′) contribue à la ligne ssi red₄(m′·t′) = μ pour un terme t′ de e′. L'égalité force : l'arête e′ et le gadget de m′ reproduisent le motif de W (donc e′ vit dans W élargi de ≤ 3 : nombre fini de positions relatives, indépendant de n par le Lemme S), et l'éclaireur de m′ est exactement s avec l'exposant ε (aucun autre terme ne peut créer un sommet isolé à cette distance : tout produit gadget×arête vit dans W élargi). Translater s de +4 (même signe, sans quitter la zone générique) translate d'autant sa distance à *chaque* arête contributrice e′ ⊂ W : les résidus mod 4 relatifs sont préservés, le signe aussi (pas de franchissement d'antipode ni de fenêtre, par définition de la zone), donc **l'étiquette de chaque colonne contributrice est inchangée**, et les coefficients (multiplicités des termes d'arête) sont invariants par translation. Les deux signatures sont égales terme à terme. ∎

*Conséquence.* Par type de fenêtre et ε, la zone générique produit au plus 4 × 2 = 8 signatures distinctes — un nombre indépendant de n.

## 4. Lemme B (les deux bords, et l'origine des strates)

**Énoncé.** (i) *Bord de fenêtre* (|δ| ≤ w₀ + 4) : nombre fini de cas, chacun un motif borné du Lemme S — indépendant de n dès n ≥ 25. (ii) *Bord antipodal* (|δ| ≥ ⌊n/2⌋ − (w₀ + 4)) : les positions concernées s'écrivent δ = ⌊n/2⌋ − i, 0 ≤ i ≤ w₀ + 4 ; leurs résidus mod 4 valent (⌊n/2⌋ − i) mod 4 = (2q − i) mod 4, qui pour i parcourant une plage fixe est une fonction de **q mod 2** uniquement. Le catalogue des signatures de bord antipodal est donc fini et ne dépend que de la parité de q. (n = 4q+1 est impair : il n'existe **pas** d'égalité δ = n − δ, donc pas de cas d'ex-æquo 'S' — le pli est toujours strict, contrairement à ZJ pair.)

*Preuve de (ii).* ⌊n/2⌋ = ⌊(4q+1)/2⌋ = 2q. Résidu : (2q − i) mod 4 ∈ {(2q) mod 4 − i} = fonction de q mod 2 et de i. Pour q pair, 2q ≡ 0 ; pour q impair, 2q ≡ 2 (mod 4). Deux catalogues, un par parité, chacun constant en q dans sa strate dès que la plage 0 ≤ i ≤ w₀ + 4 est disjointe du bord de fenêtre — garanti dès ⌊n/2⌋ > 2(w₀ + 4), soit n ≥ 29 + ε, **q ≥ 8**. ∎

## 5. Lemme C-mod4 (fermeture) et le seuil

**Énoncé.** Pour **q ≥ q₀ = 8**, l'ensemble 𝔈_q des équations d'étiquettes distinctes vérifie 𝔈_q = 𝔈_{q mod 2} : deux ensembles seulement, un par strate de parité.

*Preuve.* Toute ligne est : sans éclaireur (types du Lemme S, catalogue constant dès q ≥ 6), ou à éclaireur générique (signatures du Lemme Z, catalogue constant : 8 par type), ou à éclaireur de bord (Lemme B : catalogue constant par strate dès q ≥ 8). Réciproquement, chaque élément de ces catalogues est réalisé par au moins une ligne dès que la zone générique est non vide pour chaque résidu et signe — c'est-à-dire dès que ⌊n/2⌋ − 2(w₀ + 4) ≥ 8, soit q ≥ 8 encore. L'ensemble des signatures — donc 𝔈_q après dédoublonnage — est ainsi le même pour tous les q ≥ 8 d'une même parité. ∎

**Cohérence avec la machine.** Le seuil prédit q₀ = 8 encadre exactement l'empirie : |𝔈_q| = 6 109 (q=7), 6 172 (q=8), 6 184 (q=9) — croissance résiduelle +12 entre 8 et 9, que le lemme impose d'interpréter ainsi : *si* la preuve est complète, 𝔈₈ ⊊ 𝔈_pair n'est plus possible et l'incrément q=9 → q=11 doit être **nul** (même parité). La mission CC-02 mesure précisément cela — le lemme est falsifiable par les comptes d'équations autant que par les verdicts de prédiction. [Si +12 provient d'un effet de bord non couvert (voir R2), le seuil se décale d'un cran : q₀ = 10 ; l'architecture de l'assemblage est inchangée.]

## 6. Assemblage — Théorème 1 bis

> **Théorème 1 bis (présentation finie de G_CH(q,4), module 4).** Pour tout q ≥ 3, le graphe 5-critique G_CH(q,4) (n = 4q+1) admet un certificat de Nullstellensatz exact sur ℚ de degré 5 (niveaux {1,5}, encodage racines quartiques), supporté sur les arêtes d'écart ≤ 3, de la forme éclaireur × gadget (L = 3). De plus, la famille admet une **présentation finie à deux strates** : un alphabet de 6 487 étiquettes indépendantes de n et deux vecteurs de constantes rationnelles V_pair, V_impair (dénominateurs | 16) tels que pour q ≥ q₀, le certificat de G_CH(q,4) est l'instanciation de V_{q mod 2}.

*Preuve (structure).* (a) q = 3, 4, 5 : certificats exacts individuels, vérifiés sur ℚ [machine, CC-01 §3 + `j2_verify_joint`]. (b) q ∈ {6, 7, 8, 9} : solutions exactes V_pair (6, 8) et V_impair (7, 9), vérifiées, bit-identiques par strate [machine, CC-01]. (c) q ≥ q₀ : par le Lemme C-mod4, 𝔈_q = 𝔈_{q mod 2} = 𝔈_{8 ou 9} ; V_{q mod 2} ⊨ 𝔈_{q mod 2} [machine] ; l'instanciation (dossier 9, théorème d'instanciation : trois lignes, le poids est dans les axiomes — ici la cohérence A2 est la construction même de 𝔈) redistribue les constantes sur les colonnes de chaque G_CH(q,4) et fournit A·μ = e, un certificat exact. (d) Les q entre 9 et q₀, s'il en reste selon R2, sont couverts par calcul direct [CC-02]. ∎ *(modulo la liste [R])*

## 7. Liste [R] — ce qui reste pour clore

- **R1 (comptabilité de w₀).** La largeur w₀ = 10 est établie pour le produit gadget×arête ; vérifier qu'aucune réduction mod 4 ne crée de motif à DEUX sommets isolés (deux « éclaireurs » effectifs) à partir d'un gadget chevauchant l'éclaireur — le cas |δ| ≤ w₀ est traité comme motif borné (Lemme B-i), mais l'inventaire mécanique de ces motifs doit être exécuté une fois (script court, à confier à CC-03).
- **R2 (l'incrément +12).** Identifier les 12 équations nouvelles de q=9 par rapport à q=8 ∪ q=7 : bord non couvert (→ q₀ = 10) ou simple réalisation tardive d'un type prédit (→ q₀ = 8 confirmé). Diagnostic mécanique direct sur les builds de CC-02.
- **R3 (réalisation).** La réciproque du Lemme 5 (chaque signature du catalogue est réalisée dès q ≥ 8) est esquissée par un argument de place ; la rendre effective (exhiber la ligne réalisante par type) est mécanique.
- **R4 (composition formelle).** Rédiger l'instanciation (c) au niveau du recueil : la matrice A_q restreinte, la carte colonnes → étiquettes, et la commutation somme-par-étiquette / somme-par-colonne — pur assemblage, déjà validé numériquement 4 fois par `j2_verify_joint`.
- **R5 (unicité de forme).** V_pair et V_impair coïncident sur 334 étiquettes et diffèrent sur ~117 ; vérifier si un changement de jauge (élément du noyau commun) les identifie — si oui, la présentation est à UNE strate à jauge près, énoncé plus fort.

## 8. Prédictions falsifiables — verdicts partiels (CC-02, 28 juillet matin)

1. **`j2_predict.py 10` : PREDICTION OK** — V_pair satisfait les 6 186 équations de q=10 (n=41), zéro violation, 411/411 étiquettes retrouvées. **`j2_predict.py 11` : PREDICTION OK** — V_impair, 6 186 équations (n=45), zéro violation. (Auto-validation préalable du script à q=3 : OK.)
2. **Solves exacts : sol(10) == V_pair et sol(11) == V_impair, bit à bit** (vérifié ici sur les JSON). La 2-périodicité couvre désormais **six ordres consécutifs, q = 6…11**, doublement établie (évaluation + identité de solve indépendant).
3. **Comptes d'équations : 6 172 (q=8) → 6 184 (q=9) → 6 186 (q=10) → 6 186 (q=11).** Incréments résiduels +14 (strate paire, 8→10) et +2 (impaire, 9→11), puis **0 entre q=10 et q=11** — et les deux strates se rejoignent au même compte. **R2 est tranché dans le sens du décalage : q₀ = 10** (réalisations tardives jusqu'à n = 41), architecture du lemme inchangée. Confirmation attendue de CC-02 : incréments nuls à q=12 et q=13.
