# packages + prep -----------------------------------------------------------------------------------------------------
packages = c("tidyverse",
             "magrittr",
             "readxl",
             "Rmisc" ,
             "ggplot2",
             "reshape2",
             "lme4",
             "lmerTest",
             "modelbased",
             "ggeffects",
             "plot3D",
             "viridis",
             "quickpsy")


## Now load or install&load all
package.check <- lapply(
  packages,
  FUN = function(x) {
    if (!require(x, character.only = TRUE)) {
      install.packages(x, dependencies = TRUE)
      library(x, character.only = TRUE)
    }
  }
)
devtools::install_github("hadley/dplyr@v0.7.0")

# ggplot theme (juste un theme pour que ce soit plus joli)
customtheme <- theme_bw() +
  theme(
    panel.background = element_rect(fill = 'white'),
    axis.line = element_blank(), 
    strip.background = element_rect(fill = 'white', color = "white"),
    strip.placement = 'outside',
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    panel.spacing = unit(2, "lines"),
    axis.text = element_text(colour = "black"),
    plot.title = element_text(hjust = 0.5),
    text = element_text(size = 20)) 

palette <- c("blue", "mediumseagreen")


# data ----------------------------------------------------------------------------------------------------------------
# lit tous les fichiers dans le dossier data et les met dans un dataframe
df <-
  list.files(path = "C:/Users/grandjeamari/Documents/Travail/UCLouvain/PhD/Projet/Projet-Saccades/Analysis/Data/Radial bias", full.names = TRUE, pattern = "*.csv") %>%
  map_df(~read_csv(.))

unique(df$participant)

theSubj = 'PIBE29' #ici remplace par le nom du sujet dont tu veux ploter les donnees (ce qu'on rentre dans la dialbox psychopy)

df %<>%
  filter(participant == theSubj) # garde dans df seulement les donnees de theSubj




# Bin contrast ------------------------------------------------------------
df <- df %>%
  mutate(contrastINT = as.integer(contrast*100)) %>% 
  mutate(contrastbin = ntile(contrastINT, n=6))

# Arrange df   ------------------------------------------------------------
df <- df %>%
  mutate(
    VF =
      case_when(
        VF == "left"  ~ "Gauche",
        VF == "right" ~ "Droit",
        VF == "up" ~ "Haut",
        VF == "down" ~ "Bas",
        TRUE ~ VF
      ),
    ori = 
      case_when(
        ori == "oriH" ~ "Orientation = horizontale",
        ori == "oriV" ~ "Orientation = verticale",
        TRUE ~ ori
      )
  ) 

df$VF <- factor(df$VF, levels = c("Gauche","Droit","Haut","Bas"))




# Quickpsy Fit ---------------------------------------------------------------
df_fit <- df %>% 
  # filter(eccentricity == '15dva') %>%
  group_by(meridian, VF, ori, contrastbin) %>% 
  dplyr::summarise(meanAcc = mean(accuracy))
df_fit$VF <- factor(df_fit$VF, levels = c("Gauche","Droit","Haut","Bas"))

df_fit %<>% 
  mutate(meanAcc = ifelse(meanAcc < 0.25, 0.25, meanAcc))


# Fit and plot horizontal meridian --------------------------------------------------------------------------------------------
fitH <-
  quickpsy(
    df_fit %>% filter(meridian == "meridianH"),
    x = contrastbin,
    k = meanAcc,
    grouping = c("ori", "VF"),
    #xperimental factors
    fun = cum_normal_fun,
    #model = cumulative normal function 
    guess = 0.25,
    #chance level
    lapses = TRUE,
    #for lapse rate
    bootstrap = 'none',
    #bootstrap of parameters (swich on: 'parametric' or 'nonparametric')
    # B = 500,
    #number of bootstrap samples
    parini = list(c(1, 6), c(0.1, 8), c(0, .1)) #pas obligatoire mais pafois ça fit mieux en forçant les paramètres initiaux (sinon enlever la ligne et il a des parametres par defaut)
  )
  
# plot horizontal meridian
df %>% 
  filter(meridian == "meridianH") %>% 
  group_by(eccentricity, VF, ori, contrastbin) %>% 
  dplyr::summarise(meanAcc = mean(accuracy),
                   n = n()) %>% 
  ggplot(aes(x = contrastbin, y = meanAcc, color = ori)) +
  geom_point(aes(size = n)) +
  # geom_line() +
  geom_line (data = fitH$curves, aes(x = x, y = y, color = ori), size = 2, alpha = 0.6) +
  geom_linerange(data = fitH$thresholds, 
                 aes_string(x = "thre", ymin = fitH$guess, ymax = fitH$thresholds$prob), inherit.aes = FALSE, 
                 color = c(palette[1],palette[1],palette[2],palette[2]),
                 size = 1) +
  facet_grid(~VF) +
  geom_hline(yintercept = 0.25, color = "black", size = 0.5) +
  geom_hline(yintercept = 0.625, color = "black", linetype = "dotted", size = 0.5) +
  scale_x_continuous(breaks = seq(1, 6, 1)) +
  scale_y_continuous(breaks = c(0, 0.25, 0.5, 0.63, 0.75, 1), limits = c(0,1)) +
  scale_color_manual(values = palette) +
  scale_size(guide = 'none') +
  labs(x = "Contraste", y = "Précision moyenne") +
  customtheme +
  theme(legend.title = element_blank()) #+
  # ggtitle('Méridien horizontal') 
  

thr.H <- fitH$thresholds
thr.H %>% ggplot(aes(x = VF, y = thre, fill = ori, color = ori)) +
  geom_col(
    stat = "identity",
    position = position_dodge(width = 0.9),
    width = 0.8,
    alpha = 0.2,
    size = 1
  ) +
  scale_color_manual(values = palette) +
  scale_fill_manual(values = palette) +
  scale_y_continuous(breaks = c(0, 1, 2, 3, 4, 5, 6), limits = c(0,6)) +
  labs(x = "Champ visuel", y = "Seuil de détection") +
  customtheme +
  theme(legend.position = "none",
        legend.title = element_blank())





# Plot Vertical meridian --------------------------------------------------------------------------------------------
fitV <-
  quickpsy(
    df_fit %>% filter(meridian == "meridianV"),
    x = contrastbin,
    k = meanAcc,
    grouping = c("ori", "VF"),
    #xperimental factors
    fun = cum_normal_fun,
    #model = cumulative normal function 
    guess = 0.25,
    #chance level
    lapses = TRUE,
    #for lapse rate
    bootstrap = 'none',
    #bootstrap of parameters (swich on: 'parametric' or 'nonparametric')
    # B = 500,
    #number of bootstrap samples
    parini = list(c(1, 6), c(0.1, 8), c(0, .1)) #pas obligatoire mais pafois ça fit mieux en forçant les paramètres initiaux (sinon tu peux enlever la ligne et il a des parametres par defaut)
  )

# plot vertical meridian
df %>% 
  filter(meridian == "meridianV") %>% 
  group_by(eccentricity, VF, ori, contrastbin) %>% 
  dplyr::summarise(meanAcc = mean(accuracy),
                   n = n()) %>% 
  ggplot(aes(x = contrastbin, y = meanAcc, color = ori)) +
  geom_point(aes(size = n)) +
  geom_line (data = fitV$curves, aes(x = x, y = y, color = ori), size = 2, alpha = 0.6) +
  geom_linerange(data = fitV$thresholds, 
                 aes_string(x = "thre", ymin = fitH$guess, ymax = fitH$thresholds$prob), inherit.aes = FALSE, 
                 color = c(palette[1],palette[1],palette[2],palette[2]),
                 size = 1) +
  facet_grid(~VF) +
  geom_hline(yintercept = 0.25, color = "black", size = 0.5) +
  geom_hline(yintercept = 0.625, color = "black", linetype = "dotted", size = 0.5) +
  scale_x_continuous(breaks = seq(1, 6, 1)) +
  scale_y_continuous(breaks = c(0, 0.25, 0.5, 0.63, 0.75, 1), limits = c(0,1)) +
  scale_color_manual(values = palette) +
  scale_size(guide = 'none') +
  labs(x = "Contraste", y = "Précision moyenne") +
  customtheme +
  theme(legend.position = "none",
        legend.title = element_blank()) #+
  # ggtitle('Méridien vertical') 


thr.V <- fitV$thresholds

thr.V %>% ggplot(aes(x = VF, y = thre, fill = ori, color = ori)) +
  geom_col(
    stat = "identity",
    position = position_dodge(width = 0.9),
    width = 0.8,
    alpha = 0.2,
    size = 1
  ) +
  scale_color_manual(values = palette) +
  scale_fill_manual(values = palette) +
  scale_y_continuous(breaks = c(0, 1, 2, 3, 4, 5, 6), limits = c(0,6)) +
  labs(x = "Champ visuel", y = "Seuil de détection") +
  customtheme +
  theme(legend.position = "none",
        legend.title = element_blank()) 















# 
# # Plot staircase ------------------------------------------------------------------------------------------------------
# 
# vertical meridian
df %>%
  filter(meridian == 'meridianV') %>%
  drop_na(condition) %>%
  ggplot(aes(x = trialCount, y=contrast, color = contrastRule, group=1)) +
  geom_point() +
  geom_line() +
  facet_grid(.~condition) +
  customtheme

# horizontal meridian
df %>%
  filter(meridian == 'meridianH') %>%
  drop_na(condition) %>%
  ggplot(aes(x = trialCount, y=contrast, color = contrastRule, group=1)) +
  geom_point() +
  geom_line() +
  facet_grid(.~condition) +
  customtheme
#
# 
# # plot data / condition -----------------------------------------------------------------------------------------------
# 
# plot data horizontal meridian
df %>%
  filter(meridian == "meridianH") %>%
  group_by(eccentricity, VF, ori, contrastbin) %>%
  dplyr::summarise(meanAcc = mean(accuracy),
                   n = n()) %>%
  ggplot(aes(x = contrastbin, y = meanAcc, color = ori)) +
  geom_point(aes(size = n)) +
  geom_line() +
  facet_grid(eccentricity~VF) +
  customtheme +
  ggtitle('horizontal meridian') +
  geom_hline(yintercept = 0.25, linetype = "dashed", color = "orange", size = 1) +
  ylim(0,1)

# # plot data vertical meridian
# df %>% 
#   filter(meridian == "meridianV") %>%   
#   group_by(eccentricity, VF, ori, contrastbin) %>% 
#   dplyr::summarise(meanAcc = mean(accuracy),
#                    n = n()) %>% 
#   ggplot(aes(x = contrastbin, y = meanAcc, color = ori)) +
#   geom_point(aes(size = n)) +
#   geom_line() +
#   facet_grid(eccentricity~VF) +
#   customtheme +
#   ggtitle('vertical meridian') +
#   geom_hline(yintercept = 0.25, linetype = "dashed", color = "orange", size = 1) +
#   ylim(0,1)
# 
# 


