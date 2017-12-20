plot_functions = '''
library(phytools)
library(plotly)
library(tidyverse)
library(ggtree)

basename <- z
print(paste0('basename: ', basename))
nsnps <- a
seqlen <- b
kmer <- k
tree <- read.newick(file=paste0(basename, '.mp.treefile'))
tree_clust <- read.newick(file=paste0(basename, '.mp_clusterPicks.nwk'))
cluster_picks <- matrix(nrow = 0, ncol = 2) 
colnames(cluster_picks) <- c('Isolate', 'Cluster')
cluster_picks

for(tip in tree_clust$tip.label[grep('Clust', tree_clust$tip.label)]){
    outp_list_of_lists <- strsplit(tip, split = '_') 
    output_list <- outp_list_of_lists[[1]]
    cluster_picks <- rbind(cluster_picks, c(paste0(output_list[2:length(output_list)], collapse='_'), output_list[1]))
    }

cluster_picks <- data.frame(cluster_picks, stringsAsFactors=FALSE)
cluster_picks


#list_of_clusters <- split(cluster_picks$Isolate, cluster_picks$Cluster)
p <- ggtree(tree) %<+% cluster_picks
offst <- 0.2105*max(dist.nodes(tree))+0.1712
fntsz <- -0.005*length(tree$tip.label)+2.23817
wdth <- 4
q <- p + geom_tiplab(aes(label=label, color=Cluster), size=fntsz, linesize=0.2, align=TRUE) +
    # theme(legend.position = "right") +
    geom_tippoint(aes(color=Cluster), size=fntsz, na.rm=T) +
    geom_text2(aes(x=branch, label=as.integer(label), vjust=-0.3, hjust=1, subset=(isTip!=TRUE), na.rm=TRUE), size=fntsz, na.rm=TRUE) +
    geom_treescale(x=0.01, y =-2, offset=1, fontsize = fntsz) +
    annotate("text", x = 0.015, y=-4, label = "Substitutions per site", size=fntsz) + 
    ggtitle(label = "ML IQtree with bootstrap %, tips cluster-picked (left); fasta alignment (right)", subtitle = paste0('Clusters (coloured tips) have been picked as clades with >=95% support and divergence <= ', nsnps/seqlen*100, '%', ' (i.e., <= ', nsnps, ' SNPs in ', seqlen, ' bp)')) +
    scale_colour_brewer(palette = "Set1", na.value = "black")

#q
pdf(file=paste0(basename, '.mp.treefile.', 'div_', nsnps, 'SNPsIn', seqlen, 'bp_msa.pdf'), paper = 'a4r', width=11.69, height=8.27, onefile = TRUE)

h <- msaplot(p=q, fasta=basename, offset = offst, width = wdth, bg_line = FALSE, color=c('#f7fcfd', #white
                                                                                    '#ef3b2c', #red
                                                                                    '#41ab5d', #green
                                                                                    '#ffffbf', #yellow
                                                                                    '#4292c6', #blue
                                                                                    '#dface5',
                                                                                    '#c699cc',
                                                                                    '#ad86b2',
                                                                                    '#947399',
                                                                                    '#7c607f',
                                                                                    '#634c66',
                                                                                    '#4a394c',
                                                                                    '#312633',
                                                                                    '#181319',
                                                                                    '#000000',
                                                                                    '#f8c0ff'))
h
dev.off()


library(pheatmap)

aln <- read.dna(basename, format = 'fasta', as.character = TRUE)
snp_dists <- function(alignment, exclude_char){
    mat <- matrix(0, nrow = nrow(alignment), ncol = nrow(alignment))
    colnames(mat) <- rownames(alignment)
    rownames(mat) <- rownames(alignment)
    mat_snps <- mat
    pw_dist <- function(Aln_sub){
        len_aln <- Aln_sub[, c(which(!(Aln_sub[1,] %in% exclude_char) & !(Aln_sub[2,] %in% exclude_char))), drop=FALSE]
        n_snps <- len_aln[, c(which(len_aln[1,]!=len_aln[2,])), drop=FALSE]
        return(c(paste0('=', ncol(n_snps), '/', ncol(len_aln)), ncol(n_snps)))
    }
    for(i in 1:nrow(alignment)){
        for(j in i:nrow(alignment)){
            seq1 <- rownames(alignment)[i]
            seq2 <- rownames(alignment)[j]
            val <- pw_dist(alignment[c(i,j), , drop=FALSE])
            mat[seq1, seq2] <- val[1]
            mat[seq2, seq1] <- val[1]
            mat_snps[seq1, seq2] = as.numeric(val[2])
            mat_snps[seq2, seq1] = as.numeric(val[2])
            }
        }
    return(list(mat, mat_snps))
}

exclusions <- tolower(c(names(IUPAC_CODE_MAP)[!(names(IUPAC_CODE_MAP) %in% c('A', 'C', 'T', 'G'))], '-', '?'))

#Returns two matrices
snps <- snp_dists(aln, exclusions)
heatmap_data <- snps[[2]]

# re_name <- function(iname, trmatrix) {
#     if(iname %in% trmatrix[,1]){
#         row <- which(trmatrix[,1]==iname)
#         return(paste0(trmatrix[row,1], ' ', trmatrix[row,2])) 
#     }
#     else{
#         return(iname)
#     }
# }
# 
# colnames(heatmap_data) <- lapply(colnames(heatmap_data),
#                                  re_name,
#                                  cluster_picks)
# rownames(heatmap_data) <- lapply(rownames(heatmap_data),
#                                  re_name,
#                                  cluster_picks)

pheatmap(heatmap_data,
         show_rownames = T,
         show_colnames = T,
         display_numbers = TRUE,
         number_format = '%.0f',
         fontsize = fntsz*2,
         filename = paste0(basename,
#                            '_ClustersPicked',
#                            nsnps,
#                            'SNPsIn',
#                            seqlen,
                           '_SNPdists.pdf'),
         width=11.69,
         height=8.27)
dev.off()
write.csv(x=heatmap_data, file=paste0(basename,
#                                       '_ClustersPicked',
#                                       nsnps,
#                                       'SNPsIn',
#                                       seqlen,
                                      '_SNPdists.csv'),
          quote=FALSE)

write.csv(snps[[1]], file=paste0(basename,
#                                  '_ClustersPicked',
#                                  nsnps,
#                                  'SNPsIn',
#                                  seqlen,
                                 '_SNPcountsOverAlignLength.csv'),
          quote = FALSE)
'''