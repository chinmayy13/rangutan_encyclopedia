% Adsorption kinetics analysis for 2-naphthoxyacetic acid, pH 3 and pH 9.
% Reproduces every number in the GTF files from the raw absorbance data
% in Kinetic data.xlsx and the constants in Data Information table.docx.
%
% Chain: raw absorbance at 325 nm -> concentration (Beer-Lambert)
%        -> adsorption capacity and efficiency (mass balance)
%        -> pseudo-second-order kinetic fit (Gauss-Newton)
%
% Run this whole script in Octave. It prints the capacity/efficiency
% table for both pH conditions and the fitted qe, k2, R^2 for each.

clear; clc;

% --- Constants from Data Information table.docx ---
V = 0.120;      % volume of adsorbate, L
m = 0.1;        % mass of adsorbent, g
epsilon = 0.008; % molar extinction coefficient, L/mol/cm
l = 1;          % path length, cm

% --- Timestamps (minutes) ---
t = [0 1 3 5 7 10 15 20 30 40 50 60 80 100 120 140 180 230 290 340 400 460]';

% --- Raw absorbance at 325 nm, from Kinetic data.xlsx ---
abs_pH3 = [1.0916 1.0916 1.0912 1.0809 1.0776 1.0803 1.0757 1.0608 1.0547 ...
           1.0284 1.0177 0.9896 0.9860 0.9425 0.9057 0.8845 0.8644 0.8380 ...
           0.8033 0.7700 0.7296 0.7079]';

abs_pH9 = [1.1454 1.1454 1.1455 1.1354 1.1326 1.1263 1.1283 1.1315 1.1149 ...
           1.1070 1.0924 1.0933 1.0771 1.0731 1.0514 1.0391 1.0202 1.0011 ...
           0.9802 0.9422 0.9165 0.8790]';

function [q, eff, conc] = capacity_efficiency(abs_vals, V, m, epsilon, l)
  conc = abs_vals ./ (epsilon * l);      % Beer-Lambert: C = A / (eps * l)
  C0 = conc(1);
  q = (C0 - conc) * (V / m);             % mass balance capacity
  eff = (C0 - conc) ./ C0 * 100;         % efficiency (%)
  % Noise-floor rule: a timestamp within instrument noise can compute to
  % a small negative uptake. Report those as 0.00 / 0% instead.
  neg = q < 0;
  q(neg) = 0;
  eff(neg) = 0;
endfunction

function [qe, k2, R2] = fit_pso(t, q)
  % Pseudo-second-order model: q(t) = k2*qe^2*t / (1 + k2*qe*t)
  % Gauss-Newton fit with analytic Jacobian, no extra Octave packages needed.
  p = [max(q)*1.3; 2e-5];  % initial guess: [qe, k2]
  for iter = 1:200
    qe = p(1); k2 = p(2);
    D = 1 + k2*qe.*t;
    f = k2*qe^2.*t ./ D;
    r = q - f;
    dfdqe = k2*qe.*t.*(2 + k2*qe.*t) ./ D.^2;
    dfdk2 = qe^2.*t ./ D.^2;
    J = [dfdqe, dfdk2];
    dp = (J' * J) \ (J' * r);
    p = p + dp;
    if norm(dp) < 1e-12
      break;
    endif
  endfor
  qe = p(1); k2 = p(2);
  D = 1 + k2*qe.*t;
  f = k2*qe^2.*t ./ D;
  ss_res = sum((q - f).^2);
  ss_tot = sum((q - mean(q)).^2);
  R2 = 1 - ss_res/ss_tot;
endfunction

printf("=== pH 3 ===\n");
[q3, eff3, conc3] = capacity_efficiency(abs_pH3, V, m, epsilon, l);
printf("%6s %10s %10s %10s\n", "t(min)", "conc", "capacity", "efficiency");
for i = 1:length(t)
  printf("%6d %10.2f %10.2f %10.0f\n", t(i), conc3(i), q3(i), eff3(i));
endfor
[qe3, k2_3, R2_3] = fit_pso(t, q3);
printf("\nFitted PSO (pH 3): qe = %.2f mol/g, k2 = %.4e g/(mol*min), R^2 = %.4f\n\n", qe3, k2_3, R2_3);

printf("=== pH 9 ===\n");
[q9, eff9, conc9] = capacity_efficiency(abs_pH9, V, m, epsilon, l);
printf("%6s %10s %10s %10s\n", "t(min)", "conc", "capacity", "efficiency");
for i = 1:length(t)
  printf("%6d %10.2f %10.2f %10.0f\n", t(i), conc9(i), q9(i), eff9(i));
endfor
[qe9, k2_9, R2_9] = fit_pso(t, q9);
printf("\nFitted PSO (pH 9): qe = %.2f mol/g, k2 = %.4e g/(mol*min), R^2 = %.4f\n\n", qe9, k2_9, R2_9);

printf("=== Summary (should match the GTF files) ===\n");
printf("pH 3 last-reading capacity/efficiency: %.2f mol/g, %.0f%%\n", q3(end), eff3(end));
printf("pH 9 last-reading capacity/efficiency: %.2f mol/g, %.0f%%\n", q9(end), eff9(end));
printf("pH 3 fitted qe/k2/R2: %.1f, %.2e, %.3f\n", qe3, k2_3, R2_3);
printf("pH 9 fitted qe/k2/R2: %.1f, %.2e, %.3f\n", qe9, k2_9, R2_9);

% --- Percent improvement of pH 3 over pH 9, using the unrounded efficiency
%     values (not the table's displayed whole-number percentages) ---
cap_improvement = (q3(end) - q9(end)) / q9(end) * 100;
eff_improvement = (eff3(end) - eff9(end)) / eff9(end) * 100;
printf("Percent improvement, pH 3 over pH 9: capacity %.0f%%, efficiency %.0f%%\n", ...
       cap_improvement, eff_improvement);

% --- Speciation percentages (Henderson-Hasselbalch) ---
% fraction deprotonated = 10^(pH-pKa) / (1 + 10^(pH-pKa))
pKa = 3.55;
for pH = [3 9]
  ratio = 10^(pH - pKa);
  frac_deprot = ratio / (1 + ratio) * 100;
  frac_prot = 100 - frac_deprot;
  printf("pH %d speciation: %.0f%% protonated, %.1f%% deprotonated\n", pH, frac_prot, frac_deprot);
endfor
