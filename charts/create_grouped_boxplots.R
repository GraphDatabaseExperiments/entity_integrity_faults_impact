# Get command-line arguments
# `trailingOnly=TRUE` ensures we only get arguments after the script name.
args <- commandArgs(trailingOnly = TRUE)

# Check if the correct number of arguments are provided
if (length(args) != 3) {
  stop("Three arguments required: 1: duplication / null, 2: table / query, 3: recall / precision", call. = FALSE)
}


# Assign arguments to variables
scenario <- args[1]
dimension <- args[2]
metric <- args[3]


# Check arguments valid
valid_scenarios <- c("duplication", "null", "deep_integrity")
valid_dimensions <- c("table", "query")
valid_metrics <- c("recall", "precision")

if (!(scenario %in% valid_scenarios) || !(dimension %in% valid_dimensions) || !(metric %in% valid_metrics)){
  stop("Invalid arguments passed", call. = FALSE)
}

################
# Start script #
################

# Assign variables depending on setting
if (dimension == "query"){
  grouping_label <- "Query number"
  png_width <- 1800
  png_height <- 450
} else if (dimension == "table"){
  grouping_label <- "Table"
  png_width <- 900
  png_height <- 300
}



if (metric == "recall"){
  value_label <- "Recall"
  if (dimension == "query"){
    color_plots = "lightblue"
  } else if (dimension == "table"){
    if (scenario == "deep_integrity"){
      color_plots = c("lightblue", "lightblue", "lightblue", "lightblue")           
    }
    else{
      color_plots = c("steelblue", "steelblue", "lightblue", "lightblue", "lightblue", "lightblue", "lightblue", "lightblue")     
    }
  }
  color_means = "darkblue"
} else if (metric == "precision"){
  value_label <- "Precision"
  if (dimension == "query"){
    color_plots = "lightgreen"
  } else if (dimension == "table"){
    if (scenario == "deep_integrity"){
      color_plots = c("lightgreen", "lightgreen", "lightgreen", "lightgreen")
    }
    else{
      color_plots = c("mediumseagreen", "mediumseagreen", "lightgreen", "lightgreen", "lightgreen", "lightgreen", "lightgreen", "lightgreen")
    }
  }
  color_means = "darkgreen"
}




# Read data
file_path <- "data.csv"

# Filter data
content <- read.csv(file_path, header = TRUE, sep = ",")

content <- content[content$scenario == scenario,]
content <- content[content$factor == 1,]
content <- content[content$error == 0.1,]

content$recall <- as.numeric(as.character(content$recall))
content$precision <- as.numeric(as.character(content$precision))
content_filtered <- na.omit(content)



# Order dimension for output
if (scenario == "deep_integrity"){
  custom_levels <- c("customer", "orders", "supplier", "part")
  custom_labels <- c("c <- o", "o <- l.", "s <- ps <- l", "p <- ps <- l")
  content_filtered$table <- factor(content_filtered$table, levels = custom_levels, labels = custom_labels)
} else {
  content_filtered$table <- factor(content_filtered$table, levels = c("region", "nation", "customer", "orders", "supplier", "part", "partsupp", "lineitem"))
}
query_levels <- paste0("Q", 1:22)
content_filtered$query <- factor(content_filtered$query, levels = query_levels)



# Create new png
png(paste(scenario, "_", dimension, "_", metric, ".png", sep = ""), width = png_width, height = png_height)
par(mar = c(5, 6, 0.4, 0.2)) # change left margin and bottom margin
par(mgp = c(3.7, 1.2, 0))  # 3: distance for axis title, 1: distance for labels, 0: for axis line


# Create boxplots with means
boxplot_formula <- reformulate(dimension, metric)
boxplot(boxplot_formula,
        data = content_filtered,
        xlab = grouping_label,
        ylab = value_label,
        font.lab = 2, # label font bold
        font.axis = 2, # axis font bold
        #xlim = c(0.05, 0.05), # reduce margin inside plot on left and right
        col = color_plots,
        cex.lab = 3.2,
        cex.axis = 2.2,
        outline = FALSE)

means <- tapply(content_filtered[[metric]], content_filtered[[dimension]], mean)

points(x = 1:length(means),
       y = means,
       pch = 4,  # Plot character (0-25): 4 is cross
       col = color_means,
       cex = 2)


# Save png
dev.off()





