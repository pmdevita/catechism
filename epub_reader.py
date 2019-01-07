import epub

book  =  epub . open_epub ( 'test.epub' ) 

for  item_id ,  linear  in  book . opf . spine . itemrefs : 
    item  =  book . get_item ( item_id ) 
    # Check if linear or not 
    if  linear : 
        print  'Linear item " % s "'  %  item . href 
    else : 
        print  'Non-Linear item " % s "'  %  item .href 
    # read the content 
    data  =  book . read_item ( item )

    #print(data)