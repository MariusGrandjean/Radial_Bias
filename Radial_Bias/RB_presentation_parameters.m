%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Presentation parameters for measure_radial_bias experiment:
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% Parameters of the OLED SCREEN
d               = 80                                   % eye-screen distance in cm
dd              = 2.*d;                                % 2*d
pixelPitch      = 0.315;                               % pixel size in mm (0.315 for the Alienware OLED)
ScreenWidthpix  = 3840;                                % screen width in pixels
ScreenHeightpix = 2160;                                % screen height in pixels
ScreenWidthCm   = pixelPitch*ScreenWidthpix/10;        % screen width in cm
ScreenHeightCm  = pixelPitch*ScreenHeightpix/10;       % screen height in cm
alphaW          = 2.*atand(ScreenWidthCm/dd)           % alpha = 2arctan(w/2d) % screen width in degrees
alphaH          = 2.*atand(ScreenHeightCm/dd)          % alpha = 2arctan(w/2d) % screen height in degrees


%%% in SASAKI et al 2006
% eccentricities = 15.5°
% gabor size = 1.2°
% gabor SF = 4 cpd

%%% here:
% Eccentricities tested = 16° / 20°
% noise patch size = 3° / 6°
% gabor SF = 4 cpd


% Calculate stimulus position in pixels for ECC = 16°
Eccentricity = 16;
w = 2*d*tand(Eccentricity./2); %Ecc en cm
wPix = round(w*ScreenWidthpix/ScreenWidthCm); %Ecc en pix

% Calculate stimulus position in pixels for ECC = 20°
Eccentricity = 20;
w = 2*d*tand(Eccentricity./2); %Exc en cm
wPix = round(w*ScreenWidthpix/ScreenWidthCm); %Exc en pix





% Calculate stimulus size in pixels for desired stimulus size = 3°
dvaW            = 3;                                 % angular size (width)
dvaH            = 3;                                 % angular size (height)
realW           = dd*tand(dvaW./2);                  % gabor width in cm = 2dtan(alpha/2)
realH           = dd*tand(dvaH./2);                  % gabor height in cm = 2dtan(alpha/2)
realWpix        = round(realW*ScreenWidthpix/ScreenWidthCm) % gabor width in pixels
realHpix        = round(realH*ScreenWidthpix/ScreenWidthCm) % gabor height in pixels

% Calculate stimulus size in pixels for desired stimulus size = 6°
dvaW            = 6;                                 % angular size (width)
dvaH            = 6;                                 % angular size (height)
realW           = dd*tand(dvaW./2);                  % gabor width in cm = 2dtan(alpha/2)
realH           = dd*tand(dvaH./2);                  % gabor height in cm = 2dtan(alpha/2)
realWpix        = round(realW*ScreenWidthpix/ScreenWidthCm) % gabor width in pixels
realHpix        = round(realH*ScreenWidthpix/ScreenWidthCm) % gabor height in pixels





% Calculate the spatial frequency of the Gabor patch in cycles / pixels, for desired Gabor SF = 4 cycles / degrees
dva             = 1;                                 % 1°
dvaPix          = ScreenWidthpix/ScreenWidthCm       % How many pixels is 1°
SFdva           = 4;                                 % cycles per degrees
realSF          = dd*tand(SFdva./2)                  % cycles per cm
realSFpix       = realSF*dva/dvaPix                  % cycles per pix



% Calculate size of the grey gaussian background (and the adapter stimuli). For radius = 30°
dvaRadius       = 30;                                % angular size (radius)
dvaDiameter     = 2*dvaRadius;                       % angular size (diameter)
realDiameter    = dd*tand(dvaDiameter./2);          % diameter in cm
realDiameterPix = round(realDiameter*ScreenWidthpix/ScreenWidthCm) % diameter in pixels
% Size of the gaussian background and adapters should be realDiameterPix

