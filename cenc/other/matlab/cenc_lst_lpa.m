function cenc_lst_lpa(t2flair, reference, html_report)

if nargin<1 || isempty(t2flair)
   t2flair = fullfile(pwd,'t2flair_Affine_nu__t2flair.nii');
end
    
%if nargin<2 
%   reference = fullfile(pwd,'nu.nii');
%end

if nargin<3 || isempty(html_report)
    html_report = false;
end

disp( t2flair)
disp( reference )
disp(  html_report )
    
spm_path = fullfile(filesep,'aging1','software', 'SPM12');
lst_path = fullfile(spm_path,'toolbox', 'LST');

addpath(spm_path);
addpath(lst_path);


ps_LST_lpa(t2flair, reference, html_report)
